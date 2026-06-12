#!/usr/bin/env python3
"""Extract botanical survey data from local images with Ollama vision."""

from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
from io import StringIO
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import ollama
import pandas as pd
from PIL import Image
from tqdm import tqdm


DEFAULT_MODEL = "qwen2.5vl:3b"
DEFAULT_IMAGES_DIR = Path("images")
DEFAULT_OUTPUT_PATH = Path("output/output.csv")
DEFAULT_PLOTS_OUTPUT_PATH = Path("output/plots.csv")
DEFAULT_TABLES_OUTPUT_PATH = Path("output/tables.csv")
DEFAULT_PROMPT_FILE = Path("csv_parsing_instructions.md")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

OBSERVATION_COLUMNS = [
    "table_id",
    "image_file",
    "class",
    "order",
    "alliance",
    "association",
    "releve_id",
    "ref_code",
    "map_reference",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "species",
    "domin_value",
    "presence_binary",
    "raw_value",
    "constancy_class",
    "summary_value",
    "total_species_reported",
    "needs_review",
    "note",
]

PLOT_COLUMNS = [
    "table_id",
    "image_file",
    "releve_id",
    "ref_code",
    "map_reference",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "needs_review",
    "note",
]

TABLE_COLUMNS = [
    "table_id",
    "image_file",
    "class",
    "order",
    "alliance",
    "association",
    "n_releves",
    "total_species_reported",
    "mean_species_per_releve",
    "notes",
]

TABLE_OUTPUT_COLUMNS = [
    "row_label",
    "plot_1",
    "plot_2",
    "plot_3",
    "plot_4",
    "plot_5",
    "plot_6",
    "plot_7",
    "C",
    "D",
]

JSON_OUTPUT_COLUMNS = [
    "image_file",
    "species_name",
    "location",
    "coordinates",
    "date",
    "collector",
    "notes",
    "other_visible_fields",
    "parse_status",
    "parse_error",
    "raw_response",
]

JSON_EXTRACTION_PROMPT = """
You are digitizing geo-botanical research scans for a CSV dataset.

Read the image carefully. Return exactly one JSON object and no markdown.
Use empty strings when a field is not visible. Preserve uncertain text in notes.

Required JSON keys:
{
  "species_name": "",
  "location": "",
  "coordinates": "",
  "date": "",
  "collector": "",
  "notes": "",
  "other_visible_fields": {}
}

Rules:
- species_name should be the botanical name exactly as visible.
- coordinates should include any grid reference, latitude/longitude, or map reference.
- notes should include uncertainty, illegible text, page side, abundance, habitat, or table context.
- other_visible_fields should contain any visible labels that do not fit the required fields.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse local botanical images into CSV outputs using Ollama."
    )
    parser.add_argument("--images-dir", type=Path, default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--plots-output", type=Path, default=DEFAULT_PLOTS_OUTPUT_PATH)
    parser.add_argument("--tables-output", type=Path, default=DEFAULT_TABLES_OUTPUT_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--mode",
        choices=("tidy", "table", "json"),
        default="tidy",
        help="Use tidy mode for analysis-ready CSVs, table mode for printed-table CSV, or json mode for older specimen-style extraction.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=DEFAULT_PROMPT_FILE,
        help="Prompt file used in tidy and table modes.",
    )
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument(
        "--max-image-side",
        type=int,
        default=1600,
        help="Resize a temporary copy so the longest image side is at most this many pixels. Use 0 to send originals.",
    )
    parser.add_argument(
        "--num-predict",
        type=int,
        default=2048,
        help="Maximum response tokens Ollama can generate per image. Use 0 for the model default.",
    )
    return parser


def find_images(images_dir: Path) -> list[Path]:
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory does not exist: {images_dir}")

    images = [
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=natural_sort_key)


def natural_sort_key(path: Path) -> list[int | str]:
    parts = re.split(r"(\d+)", str(path))
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def read_prompt(prompt_file: Path) -> str:
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file does not exist: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8").strip()


def prepare_image_for_ollama(image_path: Path, max_image_side: int) -> tuple[Path, Path | None]:
    with Image.open(image_path) as image:
        image.load()

        if max_image_side <= 0 or max(image.size) <= max_image_side:
            return image_path, None

        image.thumbnail((max_image_side, max_image_side), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "L"}:
            image = image.convert("RGB")

        with tempfile.NamedTemporaryFile(
            prefix=f"{image_path.stem}_",
            suffix=".jpg",
            delete=False,
        ) as temporary_file:
            resized_path = Path(temporary_file.name)

        image.save(resized_path, format="JPEG", quality=92)
        return resized_path, resized_path


def extract_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, character in enumerate(text):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("The model response did not contain a JSON object.")


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def clean_csv_response(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:csv)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    lines = [line for line in cleaned.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if line.strip().lower().startswith("row_label,"):
            return "\n".join(lines[index:])
    return "\n".join(lines)


def parse_table_csv(text: str) -> list[dict[str, str]]:
    cleaned = clean_csv_response(text)
    reader = csv.reader(StringIO(cleaned))
    rows = list(reader)
    if not rows:
        raise ValueError("The model response did not contain CSV rows.")

    header = [cell.strip() for cell in rows[0]]
    data_rows = rows[1:] if header == TABLE_OUTPUT_COLUMNS else rows

    parsed_rows: list[dict[str, str]] = []
    for row in data_rows:
        normalized = [cell.strip() for cell in row]
        if not any(normalized):
            continue
        if len(normalized) < len(TABLE_OUTPUT_COLUMNS):
            normalized.extend([""] * (len(TABLE_OUTPUT_COLUMNS) - len(normalized)))
        if len(normalized) > len(TABLE_OUTPUT_COLUMNS):
            normalized = normalized[: len(TABLE_OUTPUT_COLUMNS) - 1] + [
                ",".join(normalized[len(TABLE_OUTPUT_COLUMNS) - 1 :])
            ]
        parsed_rows.append(dict(zip(TABLE_OUTPUT_COLUMNS, normalized, strict=True)))

    if not parsed_rows:
        raise ValueError("The model response contained only a CSV header.")
    return parsed_rows


def call_ollama_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
    response_format: str | None = None,
) -> str:
    ollama_image_path, temporary_path = prepare_image_for_ollama(image_path, max_image_side)
    options = {"temperature": 0}
    if num_predict > 0:
        options["num_predict"] = num_predict

    request: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "images": [str(ollama_image_path)],
        "options": options,
    }
    if response_format is not None:
        request["format"] = response_format

    try:
        response = ollama.generate(**request)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return response.get("response", "")


def normalize_observation(
    raw_row: dict[str, Any],
    table_row: dict[str, str],
    plots_by_releve: dict[str, dict[str, str]],
    image_file: str,
) -> dict[str, str]:
    releve_id = normalize_cell(raw_row.get("releve_id"))
    plot_row = plots_by_releve.get(releve_id, {})
    raw_value = normalize_cell(raw_row.get("raw_value"))
    domin_value = normalize_cell(raw_row.get("domin_value"))
    presence = normalize_cell(raw_row.get("presence_binary"))
    if not presence:
        presence = "0" if raw_value == "." or domin_value == "." else "1"

    return {
        "table_id": table_row["table_id"],
        "image_file": image_file,
        "class": table_row["class"],
        "order": table_row["order"],
        "alliance": table_row["alliance"],
        "association": table_row["association"],
        "releve_id": releve_id,
        "ref_code": plot_row.get("ref_code", ""),
        "map_reference": plot_row.get("map_reference", ""),
        "altitude_ft": plot_row.get("altitude_ft", ""),
        "altitude_m": plot_row.get("altitude_m", ""),
        "aspect_deg": plot_row.get("aspect_deg", ""),
        "slope_deg": plot_row.get("slope_deg", ""),
        "cover_pct": plot_row.get("cover_pct", ""),
        "plot_area_m2": plot_row.get("plot_area_m2", ""),
        "species": normalize_cell(raw_row.get("species")),
        "domin_value": domin_value,
        "presence_binary": presence,
        "raw_value": raw_value,
        "constancy_class": normalize_cell(raw_row.get("constancy_class")),
        "summary_value": normalize_cell(raw_row.get("summary_value")),
        "total_species_reported": table_row["total_species_reported"],
        "needs_review": normalize_cell(raw_row.get("needs_review")),
        "note": normalize_cell(raw_row.get("note")),
    }


def normalize_plot(
    raw_row: dict[str, Any],
    table_id: str,
    image_file: str,
) -> dict[str, str]:
    return {
        "table_id": table_id,
        "image_file": image_file,
        "releve_id": normalize_cell(raw_row.get("releve_id")),
        "ref_code": normalize_cell(raw_row.get("ref_code")),
        "map_reference": normalize_cell(raw_row.get("map_reference")),
        "altitude_ft": normalize_cell(raw_row.get("altitude_ft")),
        "altitude_m": normalize_cell(raw_row.get("altitude_m")),
        "aspect_deg": normalize_cell(raw_row.get("aspect_deg")),
        "slope_deg": normalize_cell(raw_row.get("slope_deg")),
        "cover_pct": normalize_cell(raw_row.get("cover_pct")),
        "plot_area_m2": normalize_cell(raw_row.get("plot_area_m2")),
        "needs_review": normalize_cell(raw_row.get("needs_review")),
        "note": normalize_cell(raw_row.get("note")),
    }


def normalize_table(
    raw_metadata: dict[str, Any],
    image_file: str,
) -> dict[str, str]:
    return {
        "table_id": normalize_cell(raw_metadata.get("table_id")),
        "image_file": image_file,
        "class": normalize_cell(raw_metadata.get("class")),
        "order": normalize_cell(raw_metadata.get("order")),
        "alliance": normalize_cell(raw_metadata.get("alliance")),
        "association": normalize_cell(raw_metadata.get("association")),
        "n_releves": normalize_cell(raw_metadata.get("n_releves")),
        "total_species_reported": normalize_cell(raw_metadata.get("total_species_reported")),
        "mean_species_per_releve": normalize_cell(raw_metadata.get("mean_species_per_releve")),
        "notes": normalize_cell(raw_metadata.get("notes")),
    }


def parse_tidy_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=prompt,
        max_image_side=max_image_side,
        num_predict=num_predict,
        response_format="json",
    )
    parsed = extract_json_object(raw_response)

    metadata = parsed.get("table_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    table_row = normalize_table(metadata, str(image_path))
    table_id = table_row["table_id"] or image_path.stem

    raw_plots = parsed.get("plots", [])
    if not isinstance(raw_plots, list):
        raw_plots = []
    plot_rows = [
        normalize_plot(plot, table_id, str(image_path))
        for plot in raw_plots
        if isinstance(plot, dict)
    ]
    plots_by_releve = {
        plot["releve_id"]: plot
        for plot in plot_rows
        if plot["releve_id"]
    }

    raw_observations = parsed.get("observations", [])
    if not isinstance(raw_observations, list):
        raw_observations = []
    observation_rows = [
        normalize_observation(observation, table_row, plots_by_releve, str(image_path))
        for observation in raw_observations
        if isinstance(observation, dict)
    ]

    if not plot_rows and not observation_rows:
        raise ValueError("The model response did not contain plots or observations.")

    if not table_row["table_id"]:
        table_row["table_id"] = table_id

    return [table_row], plot_rows, observation_rows


def parse_json_image(
    image_path: Path,
    model: str,
    keep_raw: bool,
    max_image_side: int,
    num_predict: int,
) -> dict[str, str]:
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=JSON_EXTRACTION_PROMPT.strip(),
        max_image_side=max_image_side,
        num_predict=num_predict,
        response_format="json",
    )
    parsed = extract_json_object(raw_response)

    return {
        "image_file": str(image_path),
        "species_name": normalize_cell(parsed.get("species_name")),
        "location": normalize_cell(parsed.get("location")),
        "coordinates": normalize_cell(parsed.get("coordinates")),
        "date": normalize_cell(parsed.get("date")),
        "collector": normalize_cell(parsed.get("collector")),
        "notes": normalize_cell(parsed.get("notes")),
        "other_visible_fields": normalize_cell(parsed.get("other_visible_fields")),
        "parse_status": "ok",
        "parse_error": "",
        "raw_response": raw_response if keep_raw else "",
    }


def parse_table_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
) -> list[dict[str, str]]:
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=prompt,
        max_image_side=max_image_side,
        num_predict=num_predict,
    )
    return parse_table_csv(raw_response)


def load_existing_rows(output_path: Path, columns: list[str]) -> pd.DataFrame:
    if not output_path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(output_path, dtype=str).fillna("")


def save_rows(rows: list[dict[str, str]], output_path: Path, columns: list[str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[columns]
    frame.to_csv(output_path, index=False)


def error_observation(image_path: Path, error: Exception) -> dict[str, str]:
    return {
        "table_id": image_path.stem,
        "image_file": str(image_path),
        "class": "",
        "order": "",
        "alliance": "",
        "association": "",
        "releve_id": "",
        "ref_code": "",
        "map_reference": "",
        "altitude_ft": "",
        "altitude_m": "",
        "aspect_deg": "",
        "slope_deg": "",
        "cover_pct": "",
        "plot_area_m2": "",
        "species": "PARSE_ERROR",
        "domin_value": "",
        "presence_binary": "",
        "raw_value": "",
        "constancy_class": "",
        "summary_value": "",
        "total_species_reported": "",
        "needs_review": "true",
        "note": str(error),
    }


def run_tidy_mode(args: argparse.Namespace, images: list[Path]) -> None:
    prompt = read_prompt(args.prompt_file)
    observation_rows = (
        load_existing_rows(args.output, OBSERVATION_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    plot_rows = (
        load_existing_rows(args.plots_output, PLOT_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    table_rows = (
        load_existing_rows(args.tables_output, TABLE_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    completed = {
        row["image_file"]
        for row in table_rows
        if row.get("image_file")
    } if args.resume else set()

    pending_images = [image for image in images if str(image) not in completed]
    for index, image_path in enumerate(tqdm(pending_images, desc="Parsing images"), start=1):
        try:
            image_tables, image_plots, image_observations = parse_tidy_image(
                image_path,
                args.model,
                prompt,
                args.max_image_side,
                args.num_predict,
            )
            table_rows.extend(image_tables)
            plot_rows.extend(image_plots)
            observation_rows.extend(image_observations)
        except Exception as error:
            observation_rows.append(error_observation(image_path, error))

        if index % args.batch_size == 0:
            save_rows(observation_rows, args.output, OBSERVATION_COLUMNS)
            save_rows(plot_rows, args.plots_output, PLOT_COLUMNS)
            save_rows(table_rows, args.tables_output, TABLE_COLUMNS)

    save_rows(observation_rows, args.output, OBSERVATION_COLUMNS)
    save_rows(plot_rows, args.plots_output, PLOT_COLUMNS)
    save_rows(table_rows, args.tables_output, TABLE_COLUMNS)
    print(
        f"Wrote {len(observation_rows)} observations to {args.output}, "
        f"{len(plot_rows)} plots to {args.plots_output}, "
        f"and {len(table_rows)} tables to {args.tables_output}."
    )


def run_table_mode(args: argparse.Namespace, images: list[Path]) -> None:
    prompt = read_prompt(args.prompt_file)
    rows = (
        load_existing_rows(args.output, TABLE_OUTPUT_COLUMNS).to_dict("records")
        if args.resume
        else []
    )

    for index, image_path in enumerate(tqdm(images, desc="Parsing images"), start=1):
        try:
            rows.extend(
                parse_table_image(
                    image_path,
                    args.model,
                    prompt,
                    args.max_image_side,
                    args.num_predict,
                )
            )
        except Exception as error:
            rows.append(
                {
                    "row_label": f"Parse error: {image_path.name}",
                    "plot_1": str(error),
                    "plot_2": "",
                    "plot_3": "",
                    "plot_4": "",
                    "plot_5": "",
                    "plot_6": "",
                    "plot_7": "",
                    "C": "",
                    "D": "",
                }
            )

        if index % args.batch_size == 0:
            save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)

    save_rows(rows, args.output, TABLE_OUTPUT_COLUMNS)
    print(f"Wrote {len(rows)} rows to {args.output}.")


def run_json_mode(args: argparse.Namespace, images: list[Path]) -> None:
    existing_frame = (
        load_existing_rows(args.output, JSON_OUTPUT_COLUMNS)
        if args.resume
        else pd.DataFrame(columns=JSON_OUTPUT_COLUMNS)
    )
    rows = existing_frame.to_dict("records")
    completed = set(existing_frame["image_file"]) if args.resume else set()
    pending_images = [image for image in images if str(image) not in completed]

    for index, image_path in enumerate(tqdm(pending_images, desc="Parsing images"), start=1):
        try:
            rows.append(
                parse_json_image(
                    image_path,
                    args.model,
                    args.keep_raw,
                    args.max_image_side,
                    args.num_predict,
                )
            )
        except Exception as error:
            rows.append(
                {
                    "image_file": str(image_path),
                    "species_name": "",
                    "location": "",
                    "coordinates": "",
                    "date": "",
                    "collector": "",
                    "notes": "",
                    "other_visible_fields": "",
                    "parse_status": "error",
                    "parse_error": str(error),
                    "raw_response": "",
                }
            )

        if index % args.batch_size == 0:
            save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)

    save_rows(rows, args.output, JSON_OUTPUT_COLUMNS)
    print(f"Wrote {len(rows)} rows to {args.output}.")


def main() -> None:
    args = build_parser().parse_args()
    images = find_images(args.images_dir)
    if args.limit is not None:
        images = images[: args.limit]

    if args.mode == "tidy":
        run_tidy_mode(args, images)
    elif args.mode == "table":
        run_table_mode(args, images)
    else:
        run_json_mode(args, images)


if __name__ == "__main__":
    main()
