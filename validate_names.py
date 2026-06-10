#!/usr/bin/env python3
"""Validate botanical species names in output/output.csv with Ollama text model."""

from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import ollama
import pandas as pd
from tqdm import tqdm


DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_INPUT_PATH = Path("output/output.csv")
DEFAULT_OUTPUT_PATH = Path("output/output_validated.csv")

VALIDATION_COLUMNS = [
    "corrected_name",
    "confidence",
    "flag",
    "note",
    "validation_status",
    "validation_error",
    "validation_raw_response",
]

VALID_CONFIDENCE = {"high", "medium", "low"}

VALIDATION_PROMPT_TEMPLATE = """
You are an expert botanist validating OCR output from geo-botanical field records.

Original species_name:
{species_name}

Context:
- location: {location}
- coordinates: {coordinates}
- date: {date}
- collector: {collector}
- notes: {notes}
- other_visible_fields: {other_visible_fields}

Return exactly one JSON object and no markdown:
{{
  "corrected_name": "",
  "confidence": "high|medium|low",
  "flag": true,
  "note": ""
}}

Rules:
- Correct obvious OCR mistakes, such as uppercase I used where lowercase l is intended.
- Prefer botanical binomial format: Genus species.
- Leave corrected_name empty when no plausible name is visible.
- Use flag=true when the name is missing, not binomial, uncertain, or needs human review.
- Use note to briefly explain the decision.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate botanical names from output/output.csv using Ollama."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    return parser


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


def normalize_flag(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = normalize_cell(value).lower()
    return "true" if text in {"true", "1", "yes", "y"} else "false"


def build_prompt(row: pd.Series) -> str:
    return VALIDATION_PROMPT_TEMPLATE.format(
        species_name=normalize_cell(row.get("species_name")),
        location=normalize_cell(row.get("location")),
        coordinates=normalize_cell(row.get("coordinates")),
        date=normalize_cell(row.get("date")),
        collector=normalize_cell(row.get("collector")),
        notes=normalize_cell(row.get("notes")),
        other_visible_fields=normalize_cell(row.get("other_visible_fields")),
    ).strip()


def validate_name(row: pd.Series, model: str, keep_raw: bool) -> dict[str, str]:
    species_name = normalize_cell(row.get("species_name"))
    if not species_name:
        return {
            "corrected_name": "",
            "confidence": "low",
            "flag": "true",
            "note": "No species name was extracted.",
            "validation_status": "ok",
            "validation_error": "",
            "validation_raw_response": "",
        }

    response = ollama.generate(
        model=model,
        prompt=build_prompt(row),
        options={"temperature": 0},
    )
    raw_response = response.get("response", "")
    parsed = extract_json_object(raw_response)

    confidence = normalize_cell(parsed.get("confidence")).lower()
    if confidence not in VALID_CONFIDENCE:
        confidence = "low"

    return {
        "corrected_name": normalize_cell(parsed.get("corrected_name")),
        "confidence": confidence,
        "flag": normalize_flag(parsed.get("flag")),
        "note": normalize_cell(parsed.get("note")),
        "validation_status": "ok",
        "validation_error": "",
        "validation_raw_response": raw_response if keep_raw else "",
    }


def load_input(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV does not exist: {input_path}")
    return pd.read_csv(input_path, dtype=str).fillna("")


def load_previous_output(output_path: Path) -> pd.DataFrame | None:
    if not output_path.exists():
        return None
    return pd.read_csv(output_path, dtype=str).fillna("")


def apply_resume_data(frame: pd.DataFrame, previous: pd.DataFrame | None) -> pd.DataFrame:
    for column in VALIDATION_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""

    if previous is None or "image_file" not in previous.columns:
        return frame

    previous_by_image = previous.drop_duplicates("image_file", keep="last").set_index("image_file")
    for index, row in frame.iterrows():
        image_file = row.get("image_file", "")
        if image_file not in previous_by_image.index:
            continue
        for column in VALIDATION_COLUMNS:
            if column in previous_by_image.columns:
                frame.at[index, column] = previous_by_image.at[image_file, column]
    return frame


def save_frame(frame: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)


def main() -> None:
    args = build_parser().parse_args()
    frame = load_input(args.input)
    if args.limit is not None:
        frame = frame.head(args.limit).copy()

    previous = load_previous_output(args.output) if args.resume else None
    frame = apply_resume_data(frame, previous)

    for index in tqdm(frame.index, desc="Validating names"):
        if args.resume and normalize_cell(frame.at[index, "validation_status"]) == "ok":
            continue

        try:
            validation = validate_name(frame.loc[index], args.model, args.keep_raw)
        except Exception as error:
            validation = {
                "corrected_name": "",
                "confidence": "low",
                "flag": "true",
                "note": "Validation failed; review manually.",
                "validation_status": "error",
                "validation_error": str(error),
                "validation_raw_response": "",
            }

        for column, value in validation.items():
            frame.at[index, column] = value

        completed_count = list(frame.index).index(index) + 1
        if completed_count % args.batch_size == 0:
            save_frame(frame, args.output)

    save_frame(frame, args.output)
    print(f"Wrote {len(frame)} rows to {args.output}.")


if __name__ == "__main__":
    main()
