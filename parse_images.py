#!/usr/bin/env python3
"""Extract geo-botanical specimen data from local images with Ollama vision."""

from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import ollama
import pandas as pd
from PIL import Image
from tqdm import tqdm


DEFAULT_MODEL = "qwen2-vl:7b"
DEFAULT_IMAGES_DIR = Path("images")
DEFAULT_OUTPUT_PATH = Path("output/output.csv")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

OUTPUT_COLUMNS = [
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

EXTRACTION_PROMPT = """
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
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    return parser


def find_images(images_dir: Path) -> list[Path]:
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory does not exist: {images_dir}")

    return sorted(
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def check_image_can_open(image_path: Path) -> None:
    with Image.open(image_path) as image:
        image.verify()


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


def parse_image(image_path: Path, model: str, keep_raw: bool) -> dict[str, str]:
    check_image_can_open(image_path)

    response = ollama.generate(
        model=model,
        prompt=EXTRACTION_PROMPT.strip(),
        images=[str(image_path)],
        options={"temperature": 0},
    )
    raw_response = response.get("response", "")
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


def load_existing_rows(output_path: Path) -> pd.DataFrame:
    if not output_path.exists():
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.read_csv(output_path, dtype=str).fillna("")


def save_rows(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    for column in OUTPUT_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[OUTPUT_COLUMNS]
    frame.to_csv(output_path, index=False)


def main() -> None:
    args = build_parser().parse_args()
    images = find_images(args.images_dir)
    if args.limit is not None:
        images = images[: args.limit]

    existing_frame = load_existing_rows(args.output)
    rows = existing_frame.to_dict("records")
    completed = set(existing_frame["image_file"]) if args.resume else set()

    pending_images = [image for image in images if str(image) not in completed]
    if not pending_images:
        save_rows(rows, args.output)
        print(f"No new images to parse. Wrote {len(rows)} rows to {args.output}.")
        return

    for index, image_path in enumerate(tqdm(pending_images, desc="Parsing images"), start=1):
        try:
            row = parse_image(image_path, args.model, args.keep_raw)
        except Exception as error:
            row = {
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
        rows.append(row)

        if index % args.batch_size == 0:
            save_rows(rows, args.output)

    save_rows(rows, args.output)
    print(f"Wrote {len(rows)} rows to {args.output}.")


if __name__ == "__main__":
    main()
