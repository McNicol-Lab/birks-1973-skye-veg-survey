#!/usr/bin/env python3
"""Extract botanical table data from local images with Ollama vision."""

from __future__ import annotations

import argparse
import csv
import json
import re
import tempfile
from json import JSONDecodeError
from pathlib import Path
from io import StringIO
from typing import Any

import ollama
import pandas as pd
from PIL import Image
from tqdm import tqdm


DEFAULT_MODEL = "qwen2.5vl:3b"
DEFAULT_IMAGES_DIR = Path("images")
DEFAULT_OUTPUT_PATH = Path("output/output.csv")
DEFAULT_PROMPT_FILE = Path("csv_parsing_instructions.md")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

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
        description="Parse local botanical images into output/output.csv using Ollama."
    )
    parser.add_argument("--images-dir", type=Path, default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--mode",
        choices=("table", "json"),
        default="table",
        help="Use table mode for vegetation tables or json mode for older specimen-style extraction.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=DEFAULT_PROMPT_FILE,
        help="Prompt file used in table mode.",
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
        default=512,
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

    row = {
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
    return row


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


def main() -> None:
    args = build_parser().parse_args()
    images = find_images(args.images_dir)
    if args.limit is not None:
        images = images[: args.limit]

    output_columns = TABLE_OUTPUT_COLUMNS if args.mode == "table" else JSON_OUTPUT_COLUMNS
    table_prompt = read_prompt(args.prompt_file) if args.mode == "table" else ""

    existing_frame = (
        load_existing_rows(args.output, output_columns)
        if args.resume
        else pd.DataFrame(columns=output_columns)
    )
    rows = existing_frame.to_dict("records")
    completed = set(existing_frame["image_file"]) if args.resume and args.mode == "json" else set()

    pending_images = [image for image in images if str(image) not in completed]
    if not pending_images:
        save_rows(rows, args.output, output_columns)
        print(f"No new images to parse. Wrote {len(rows)} rows to {args.output}.")
        return

    for index, image_path in enumerate(tqdm(pending_images, desc="Parsing images"), start=1):
        try:
            if args.mode == "table":
                image_rows = parse_table_image(
                    image_path,
                    args.model,
                    table_prompt,
                    args.max_image_side,
                    args.num_predict,
                )
                rows.extend(image_rows)
            else:
                row = parse_json_image(
                    image_path,
                    args.model,
                    args.keep_raw,
                    args.max_image_side,
                    args.num_predict,
                )
                rows.append(row)
        except Exception as error:
            if args.mode == "table":
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
            else:
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
            save_rows(rows, args.output, output_columns)

    save_rows(rows, args.output, output_columns)
    print(f"Wrote {len(rows)} rows to {args.output}.")


if __name__ == "__main__":
    main()
