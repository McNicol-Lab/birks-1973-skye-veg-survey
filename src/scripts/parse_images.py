#!/usr/bin/env python3
"""Extract botanical survey data from local images with Ollama vision.

This is the main digitizing script.

It runs in tidy mode:
- tidy: the preferred mode. It writes analysis-ready CSVs:
  output/output.csv for the scientific species observations,
  output/image_tracking.csv for simple image-level progress.

The current research goal is tidy mode because it is easiest to analyze later
with pandas, ordination, richness calculations, and resurvey comparisons.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import tempfile
from datetime import datetime, timezone
from io import StringIO
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import ollama
import pandas as pd
from PIL import Image


# Fallback model used when no better model is detected from ollama list.
# qwen2.5vl:3b works on low-RAM machines but under-extracts dense tables.
DEFAULT_MODEL = "qwen2.5vl:3b"

# Ordered preference list: strongest document-OCR vision model first.
# The script auto-detects the best installed model at startup.
# Pull your preferred model once with: ollama pull qwen2.5vl:72b
PREFERRED_MODELS = [
    "qwen2.5vl:72b",
    "llama3.2-vision:90b",
    "qwen2.5vl:32b",
    "qwen2.5vl:7b",
    "qwen2.5vl:3b",
]

DEFAULT_IMAGES_DIR = Path("images")
DEFAULT_OUTPUT_PATH = Path("output/output.csv")
DEFAULT_TRACKING_OUTPUT_PATH = Path("output/image_tracking.csv")
DEFAULT_PROMPT_FILE = Path("prompts/csv_parsing_instructions.md")
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# Columns for the preferred long-format observation CSV.
# One row means: one species in one plot/releve.
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
    "os_grid_square",
    "os_grid_reference",
    "easting",
    "northing",
    "latitude",
    "longitude",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "species_reported",
    "species",
    "domin_value",
    "domin_cover_min_pct",
    "domin_cover_max_pct",
    "presence_binary",
    "raw_value",
    "constancy_class",
    "summary_value",
    "total_species_reported",
    "needs_review",
    "note",
]

# Columns for plot/releve metadata.
# These describe each plot once, instead of repeating them by species.
PLOT_COLUMNS = [
    "table_id",
    "image_file",
    "releve_id",
    "ref_code",
    "map_reference",
    "os_grid_square",
    "os_grid_reference",
    "easting",
    "northing",
    "latitude",
    "longitude",
    "altitude_ft",
    "altitude_m",
    "aspect_deg",
    "slope_deg",
    "cover_pct",
    "plot_area_m2",
    "species_reported",
    "needs_review",
    "note",
]

# Columns for table-level metadata.
# These describe one printed table or association page.
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

# Columns for the simple image-level tracking CSV.
# One row means: one source image and its current extraction status.
TRACKING_COLUMNS = [
    "image_file",
    "image_number",
    "status",
    "last_attempt_at",
    "error_type",
    "error_message",
    "observations_added",
    "plots_detected",
    "tables_detected",
    "note",
]

# Columns for the older printed-table reconstruction mode.
# This keeps the visual table shape but is less useful for analysis.
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

# Columns for the older specimen-style JSON mode.
# This is kept for comparison but is not the current target.
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


def detect_best_available_model() -> str:
    """Return the strongest Qwen2.5-VL model currently installed in Ollama.

    Checks `ollama list` and walks PREFERRED_MODELS in order. Falls back to
    DEFAULT_MODEL when Ollama is not running or no preferred model is found.
    """
    try:
        response = ollama.list()
        # ollama Python SDK may return an object or a plain dict depending on version.
        models_list = getattr(response, "models", None) or response.get("models", [])
        installed: set[str] = set()
        for m in models_list:
            name = (
                getattr(m, "model", None)
                or (m.get("model") if isinstance(m, dict) else None)
                or getattr(m, "name", None)
                or (m.get("name") if isinstance(m, dict) else None)
                or ""
            )
            if name:
                installed.add(name)
        for preferred in PREFERRED_MODELS:
            if preferred in installed:
                return preferred
            # also match without tag (e.g. "qwen2.5vl" matches "qwen2.5vl:7b-q4_K_M")
            base = preferred.split(":")[0].lower()
            for name in sorted(installed):
                if name.lower().startswith(base + ":"):
                    return name
    except Exception:
        pass
    return DEFAULT_MODEL


def build_parser() -> argparse.ArgumentParser:
    """Define all command-line options for the script.

    argparse turns terminal flags like --limit 5 into Python values.
    Keeping these options here makes the script reusable for small tests,
    resumed runs, and full-batch processing.
    """
    parser = argparse.ArgumentParser(
        description="Parse local botanical images into CSV outputs using Ollama."
    )
    parser.add_argument("--images-dir", type=Path, default=DEFAULT_IMAGES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--tracking-output", type=Path, default=DEFAULT_TRACKING_OUTPUT_PATH)
    parser.add_argument(
        "--model",
        default=None,
        help=(
            "Ollama model to use. Omit to auto-detect the strongest available "
            "Qwen2.5-VL model from ollama list. Pass an explicit name to override."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=("tidy",),
        default="tidy",
        help="Use tidy mode for the single analysis-ready output.csv file.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        default=DEFAULT_PROMPT_FILE,
        help="Prompt file used for tidy extraction.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Retained for command compatibility. Durable runs now save after every image.",
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Skip this many naturally sorted images before applying --limit. Example: --skip 5 --limit 10 parses images 6-15.",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="With --resume, retry images marked unsuccessful in image_tracking.csv.",
    )
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument(
        "--max-image-side",
        type=int,
        default=0,
        help=(
            "Resize a temporary copy so the longest image side is at most this many pixels. "
            "Default is 0 (send at full resolution). Use a positive number only when RAM is "
            "constrained (e.g. --max-image-side 1600 for an 8GB machine)."
        ),
    )
    parser.add_argument(
        "--num-predict",
        type=int,
        default=16384,
        help="Maximum response tokens Ollama can generate per image. Use 0 for the model default.",
    )
    parser.add_argument(
        "--num-ctx",
        type=int,
        default=32768,
        help=(
            "Context window size in tokens. Must be large enough to hold the prompt, "
            "image tokens, AND the full JSON response. Ollama defaults to only 4096, "
            "which silently truncates big tables and makes them look like failed reads. "
            "Use 0 for the model default."
        ),
    )
    parser.add_argument(
        "--no-auto-rotate",
        action="store_true",
        default=False,
        help="Disable automatic rotation correction for landscape-orientation scan pages.",
    )
    parser.add_argument(
        "--tile",
        action="store_true",
        default=False,
        help=(
            "Split wide tables into header + left/right matrix tiles and upscale each "
            "tile ~2.5× before sending to the model. Improves accuracy on tables with "
            ">10 releve columns. Requires more RAM and more Ollama calls per image."
        ),
    )
    parser.add_argument(
        "--verify-counts",
        action="store_true",
        default=False,
        help=(
            "After extraction, cross-check per-releve species counts against the printed "
            "Total-number-of-species row. Logs a warning and sets needs_review when counts "
            "diverge by more than 2."
        ),
    )
    return parser


def find_images(images_dir: Path) -> list[Path]:
    """Find all supported image files and return them in natural order.

    Natural order matters because filenames like image_10 should come after
    image_2, not immediately after image_1.
    """
    if not images_dir.exists():
        raise FileNotFoundError(f"Images directory does not exist: {images_dir}")

    images = [
        path
        for path in images_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(images, key=natural_sort_key)


def natural_sort_key(path: Path) -> list[int | str]:
    """Split a filename into text and number pieces for human-style sorting."""
    parts = re.split(r"(\d+)", str(path))
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def read_prompt(prompt_file: Path) -> str:
    """Load the extraction prompt that tells the model what to return."""
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file does not exist: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8").strip()


def prepare_image_for_ollama(
    image_path: Path,
    max_image_side: int,
    auto_rotate: bool = True,
) -> tuple[Path, Path | None]:
    """Create a pre-processed temporary image for Ollama.

    Changes applied in order: (1) rotate landscape pages to portrait when
    auto_rotate is True, (2) resize if max_image_side > 0 and the image
    exceeds that limit. The original file is never modified.

    Returns (send_path, cleanup_path). cleanup_path is None when the original
    file is returned unchanged so the caller knows not to delete it.
    """
    with Image.open(image_path) as image:
        image.load()

        w, h = image.size
        modified = False

        # Rotate landscape pages to portrait. A page that is significantly wider
        # than it is tall is almost certainly a rotated scan (e.g. Table 4.8 or
        # Tables 4.50/4.51). Rotating 90° counter-clockwise puts the column
        # headers at the top where the model expects them.
        if auto_rotate and w > h * 1.35:
            image = image.rotate(90, expand=True)
            w, h = image.size
            modified = True

        # A max side of 0 means "do not resize — send full resolution".
        needs_resize = max_image_side > 0 and max(image.size) > max_image_side
        if needs_resize:
            image.thumbnail((max_image_side, max_image_side), Image.Resampling.LANCZOS)
            modified = True

        if not modified:
            return image_path, None

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
    """Pull the first valid JSON object out of a model response.

    Local models sometimes add text before or after JSON. This scans forward
    until it finds a parseable object, instead of failing on the first extra
    character.
    """
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
    """Convert any extracted value into a clean string for CSV writing."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def normalize_table_id(value: Any, fallback: str) -> str:
    """Return table ids in a stable machine-readable form like table_4_1."""
    text = normalize_cell(value).lower()
    match = re.search(r"table\s+(\d+)\.(\d+)", text)
    if match:
        return f"table_{match.group(1)}_{match.group(2)}"

    cleaned = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return cleaned or fallback


def domin_cover_range(domin_value: str) -> tuple[str, str]:
    """Convert Domin scale categories into approximate percent-cover ranges.

    Values 1-10 follow the 10-point Domin scale Gavin provided. A period means
    the species was not detected, so its cover range is 0-0. Presence-only
    marks like x do not have a cover range, so those stay blank.
    """
    ranges = {
        "1": ("0", "4"),
        "2": ("0", "4"),
        "3": ("0", "4"),
        "4": ("4", "10"),
        "5": ("10", "25"),
        "6": ("25", "33"),
        "7": ("33", "50"),
        "8": ("50", "75"),
        "9": ("75", "90"),
        "10": ("90", "100"),
        ".": ("0", "0"),
    }
    return ranges.get(domin_value.strip(), ("", ""))


def normalize_os_grid_square(value: Any) -> str:
    """Keep only a valid two-letter British National Grid square code."""
    text = normalize_cell(value).upper().replace(" ", "")
    return text if re.fullmatch(r"[A-HJ-Z]{2}", text) else ""


def normalize_map_reference(value: Any) -> str:
    """Keep map reference digits only, for example 504446."""
    return re.sub(r"\D", "", normalize_cell(value))


def build_os_grid_reference(os_grid_square: str, map_reference: str) -> str:
    """Combine grid square and numeric reference, for example NG504446."""
    if not os_grid_square or not map_reference:
        return ""
    return f"{os_grid_square}{map_reference}"


def os_grid_to_easting_northing(os_grid_square: str, map_reference: str) -> tuple[str, str]:
    """Convert a British National Grid reference into easting/northing metres.

    The two-letter grid square gives the 100 km square. The numeric reference
    gives the finer easting/northing inside that square. Six digits means
    100 m precision, eight digits means 10 m precision, and ten digits means
    1 m precision.
    """
    square = normalize_os_grid_square(os_grid_square)
    digits = normalize_map_reference(map_reference)
    if not square or len(digits) % 2 != 0 or len(digits) < 2:
        return "", ""

    letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    first = letters.find(square[0])
    second = letters.find(square[1])
    if first < 0 or second < 0:
        return "", ""

    easting_100km = ((first - 2) % 5) * 5 + (second % 5)
    northing_100km = 19 - (first // 5) * 5 - (second // 5)

    half = len(digits) // 2
    easting_digits = digits[:half]
    northing_digits = digits[half:]
    scale = 10 ** (5 - half)

    easting = easting_100km * 100000 + int(easting_digits) * scale
    northing = northing_100km * 100000 + int(northing_digits) * scale
    return str(easting), str(northing)


def osgb36_to_wgs84(easting: str, northing: str) -> tuple[str, str]:
    """Convert British National Grid easting/northing to WGS84 lat/lon.

    This is an offline implementation of the standard OSGB36 to WGS84
    transformation, so the pipeline can run without calling an external API.
    """
    if not easting or not northing:
        return "", ""

    easting_float = float(easting)
    northing_float = float(northing)

    airy_a = 6377563.396
    airy_b = 6356256.909
    f0 = 0.9996012717
    lat0 = math.radians(49)
    lon0 = math.radians(-2)
    n0 = -100000
    e0 = 400000
    e2 = 1 - (airy_b * airy_b) / (airy_a * airy_a)
    n = (airy_a - airy_b) / (airy_a + airy_b)

    lat = lat0
    meridional_arc = 0.0
    while northing_float - n0 - meridional_arc >= 0.00001:
        lat = (northing_float - n0 - meridional_arc) / (airy_a * f0) + lat
        ma = (1 + n + 1.25 * n**2 + 1.25 * n**3) * (lat - lat0)
        mb = (3 * n + 3 * n**2 + 2.625 * n**3) * math.sin(lat - lat0) * math.cos(lat + lat0)
        mc = (1.875 * n**2 + 1.875 * n**3) * math.sin(2 * (lat - lat0)) * math.cos(2 * (lat + lat0))
        md = (35 / 24 * n**3) * math.sin(3 * (lat - lat0)) * math.cos(3 * (lat + lat0))
        meridional_arc = airy_b * f0 * (ma - mb + mc - md)

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    nu = airy_a * f0 / math.sqrt(1 - e2 * sin_lat**2)
    rho = airy_a * f0 * (1 - e2) / (1 - e2 * sin_lat**2) ** 1.5
    eta2 = nu / rho - 1
    tan_lat = math.tan(lat)
    sec_lat = 1 / cos_lat
    d_easting = easting_float - e0

    vii = tan_lat / (2 * rho * nu)
    viii = tan_lat / (24 * rho * nu**3) * (5 + 3 * tan_lat**2 + eta2 - 9 * tan_lat**2 * eta2)
    ix = tan_lat / (720 * rho * nu**5) * (61 + 90 * tan_lat**2 + 45 * tan_lat**4)
    x = sec_lat / nu
    xi = sec_lat / (6 * nu**3) * (nu / rho + 2 * tan_lat**2)
    xii = sec_lat / (120 * nu**5) * (5 + 28 * tan_lat**2 + 24 * tan_lat**4)
    xiia = sec_lat / (5040 * nu**7) * (61 + 662 * tan_lat**2 + 1320 * tan_lat**4 + 720 * tan_lat**6)

    osgb_lat = lat - vii * d_easting**2 + viii * d_easting**4 - ix * d_easting**6
    osgb_lon = lon0 + x * d_easting - xi * d_easting**3 + xii * d_easting**5 - xiia * d_easting**7
    wgs_lat, wgs_lon = helmert_osgb36_to_wgs84(osgb_lat, osgb_lon)
    return f"{wgs_lat:.6f}", f"{wgs_lon:.6f}"


def helmert_osgb36_to_wgs84(lat: float, lon: float) -> tuple[float, float]:
    """Apply the OSGB36 to WGS84 Helmert transform."""
    airy_a = 6377563.396
    airy_b = 6356256.909
    wgs_a = 6378137.0
    wgs_b = 6356752.3141

    x, y, z = lat_lon_to_cartesian(lat, lon, airy_a, airy_b)
    tx, ty, tz = 446.448, -125.157, 542.060
    rx = math.radians(0.1502 / 3600)
    ry = math.radians(0.2470 / 3600)
    rz = math.radians(0.8421 / 3600)
    s = -20.4894 * 1e-6

    x2 = tx + (1 + s) * x - rz * y + ry * z
    y2 = ty + rz * x + (1 + s) * y - rx * z
    z2 = tz - ry * x + rx * y + (1 + s) * z
    return cartesian_to_lat_lon(x2, y2, z2, wgs_a, wgs_b)


def lat_lon_to_cartesian(lat: float, lon: float, axis_a: float, axis_b: float) -> tuple[float, float, float]:
    """Convert latitude/longitude radians to Cartesian x/y/z."""
    e2 = 1 - (axis_b * axis_b) / (axis_a * axis_a)
    nu = axis_a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    x = nu * math.cos(lat) * math.cos(lon)
    y = nu * math.cos(lat) * math.sin(lon)
    z = (1 - e2) * nu * math.sin(lat)
    return x, y, z


def cartesian_to_lat_lon(x: float, y: float, z: float, axis_a: float, axis_b: float) -> tuple[float, float]:
    """Convert Cartesian x/y/z to latitude/longitude decimal degrees."""
    e2 = 1 - (axis_b * axis_b) / (axis_a * axis_a)
    p = math.sqrt(x * x + y * y)
    lat = math.atan2(z, p * (1 - e2))
    previous_lat = 0.0
    while abs(lat - previous_lat) > 1e-12:
        previous_lat = lat
        nu = axis_a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
        lat = math.atan2(z + e2 * nu * math.sin(lat), p)
    lon = math.atan2(y, x)
    return math.degrees(lat), math.degrees(lon)


def clean_csv_response(text: str) -> str:
    """Remove markdown wrappers and keep the CSV-looking part of a response."""
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
    """Parse older printed-table CSV output into row dictionaries.

    This mode is kept because it can be useful for debugging OCR alignment.
    It is not the preferred final research format.
    """
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


def prepare_image_tiles(
    image_path: Path,
    max_image_side: int,
    auto_rotate: bool = True,
) -> list[tuple[Path, Path | None]]:
    """Split a wide-column table into upscaled header + matrix tiles.

    Tiling is only applied when the page (after rotation) is still wide
    relative to its height — i.e. a page with many releve columns that a
    single downscaled view would make too small to read accurately. Each tile
    is upscaled ~2.5× so fine print is large enough for the vision model.

    Returns a list of (send_path, cleanup_path) pairs in order:
      [0] header tile — top 18 % of page (releve IDs, map refs, metadata rows)
      [1] matrix-left tile — left half of species × releve matrix
      [2] matrix-right tile — right half of species × releve matrix

    Falls back to a single-image list when the page is portrait-orientation
    (no tiling needed).
    """
    with Image.open(image_path) as image:
        image.load()
        w, h = image.size

        # Rotate landscape scans first.
        if auto_rotate and w > h * 1.35:
            image = image.rotate(90, expand=True)
            w, h = image.size

        # Only tile tall-but-wide pages (after rotation a wide table still has
        # many columns — roughly >1.15:1 width-to-height after rotation).
        if w <= h * 1.15:
            # Portrait or near-square — a single image is fine.
            return [prepare_image_for_ollama(image_path, max_image_side, auto_rotate)]

        tiles: list[tuple[Path, Path | None]] = []
        UPSCALE = 2.5
        QUALITY = 95
        OVERLAP = 0.10  # column overlap between left and right matrix tiles

        regions = [
            ("hdr", (0, 0, w, int(h * 0.18))),
            ("mtxL", (0, int(h * 0.18), int(w * (0.5 + OVERLAP)), h)),
            ("mtxR", (int(w * (0.5 - OVERLAP)), int(h * 0.18), w, h)),
        ]

        for label, box in regions:
            tile = image.crop(box)
            new_w = int(tile.width * UPSCALE)
            new_h = int(tile.height * UPSCALE)
            if max_image_side > 0:
                scale = min(max_image_side / max(new_w, new_h), UPSCALE)
                new_w = max(1, int(tile.width * scale))
                new_h = max(1, int(tile.height * scale))
            tile = tile.resize((new_w, new_h), Image.Resampling.LANCZOS)
            if tile.mode not in {"RGB", "L"}:
                tile = tile.convert("RGB")
            with tempfile.NamedTemporaryFile(
                prefix=f"{image_path.stem}_{label}_",
                suffix=".jpg",
                delete=False,
            ) as tf:
                tile_path = Path(tf.name)
            tile.save(tile_path, format="JPEG", quality=QUALITY)
            tiles.append((tile_path, tile_path))

    return tiles


def verify_observation_counts(
    plot_rows: list[dict[str, str]],
    observation_rows: list[dict[str, str]],
) -> list[str]:
    """Cross-check per-releve observation counts against species_reported.

    Returns a list of issue strings. An empty list means all counts reconcile
    or no species_reported values were available to check against.
    """
    from collections import Counter

    issues: list[str] = []
    obs_per_releve: Counter[str] = Counter(
        r["releve_id"] for r in observation_rows if r.get("releve_id")
    )
    for plot in plot_rows:
        rid = plot.get("releve_id", "").strip()
        reported = plot.get("species_reported", "").strip()
        if not rid or not reported:
            continue
        try:
            expected = int(reported)
        except ValueError:
            continue
        actual = obs_per_releve.get(rid, 0)
        if abs(actual - expected) > 2:
            issues.append(
                f"releve {rid}: species_reported={expected} but extracted {actual} observations"
            )
    return issues


def call_ollama_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
    response_format: str | None = None,
    num_ctx: int = 0,
    auto_rotate: bool = True,
) -> str:
    """Send one image and one prompt to Ollama, then return the model text.

    This is the only function that talks directly to Ollama. Keeping the
    Ollama call in one place makes resizing, token limits, and cleanup easier
    to reason about.

    num_ctx sets the context window. Ollama's default is only 4096 tokens, which
    is too small once the prompt plus the image plus a large JSON response are
    added together. Big tables overflow it and come back empty or truncated, so
    the caller should pass a generous value.
    """
    ollama_image_path, temporary_path = prepare_image_for_ollama(image_path, max_image_side, auto_rotate)
    options = {"temperature": 0}
    if num_predict > 0:
        options["num_predict"] = num_predict
    if num_ctx > 0:
        options["num_ctx"] = num_ctx

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
        # Delete temporary resized images even if Ollama errors.
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return response.get("response", "")


def normalize_observation(
    raw_row: dict[str, Any],
    table_row: dict[str, str],
    plots_by_releve: dict[str, dict[str, str]],
    image_file: str,
) -> dict[str, str]:
    """Turn one model observation into one clean output/output.csv row.

    The model only has to provide the species, releve id, and cell value.
    This function adds table metadata and plot metadata so every observation
    row is self-contained and easy to analyze later.
    """
    releve_id = normalize_cell(raw_row.get("releve_id"))
    plot_row = plots_by_releve.get(releve_id, {})
    raw_value = normalize_cell(raw_row.get("raw_value"))
    domin_value = normalize_cell(raw_row.get("domin_value"))
    cover_min, cover_max = domin_cover_range(domin_value)
    presence = normalize_cell(raw_row.get("presence_binary"))

    # If the model forgets the presence flag, infer it from the extracted cell.
    # "." means absent. Anything else is treated as present unless reviewed.
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
        "os_grid_square": plot_row.get("os_grid_square", ""),
        "os_grid_reference": plot_row.get("os_grid_reference", ""),
        "easting": plot_row.get("easting", ""),
        "northing": plot_row.get("northing", ""),
        "latitude": plot_row.get("latitude", ""),
        "longitude": plot_row.get("longitude", ""),
        "altitude_ft": plot_row.get("altitude_ft", ""),
        "altitude_m": plot_row.get("altitude_m", ""),
        "aspect_deg": plot_row.get("aspect_deg", ""),
        "slope_deg": plot_row.get("slope_deg", ""),
        "cover_pct": plot_row.get("cover_pct", ""),
        "plot_area_m2": plot_row.get("plot_area_m2", ""),
        "species_reported": plot_row.get("species_reported", ""),
        "species": normalize_cell(raw_row.get("species")),
        "domin_value": domin_value,
        "domin_cover_min_pct": cover_min,
        "domin_cover_max_pct": cover_max,
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
    """Normalize one model plot object so observations can inherit metadata."""
    map_reference = normalize_map_reference(raw_row.get("map_reference"))
    os_grid_square = normalize_os_grid_square(raw_row.get("os_grid_square"))
    os_grid_reference = build_os_grid_reference(os_grid_square, map_reference)
    easting, northing = os_grid_to_easting_northing(os_grid_square, map_reference)
    latitude = normalize_cell(raw_row.get("latitude"))
    longitude = normalize_cell(raw_row.get("longitude"))
    if not latitude and not longitude:
        latitude, longitude = osgb36_to_wgs84(easting, northing)

    return {
        "table_id": table_id,
        "image_file": image_file,
        "releve_id": normalize_cell(raw_row.get("releve_id")),
        "ref_code": normalize_cell(raw_row.get("ref_code")),
        "map_reference": map_reference,
        "os_grid_square": os_grid_square,
        "os_grid_reference": os_grid_reference,
        "easting": easting,
        "northing": northing,
        "latitude": latitude,
        "longitude": longitude,
        "altitude_ft": normalize_cell(raw_row.get("altitude_ft")),
        "altitude_m": normalize_cell(raw_row.get("altitude_m")),
        "aspect_deg": normalize_cell(raw_row.get("aspect_deg")),
        "slope_deg": normalize_cell(raw_row.get("slope_deg")),
        "cover_pct": normalize_cell(raw_row.get("cover_pct")),
        "plot_area_m2": normalize_cell(raw_row.get("plot_area_m2")),
        "species_reported": normalize_cell(raw_row.get("species_reported")),
        "needs_review": normalize_cell(raw_row.get("needs_review")),
        "note": normalize_cell(raw_row.get("note")),
    }


def normalize_table(
    raw_metadata: dict[str, Any],
    image_file: str,
) -> dict[str, str]:
    """Normalize table-level model metadata for output.csv rows."""
    return {
        "table_id": normalize_table_id(raw_metadata.get("table_id"), Path(image_file).stem),
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


def build_previous_page_context(
    prev_table_row: dict[str, str] | None,
    prev_plot_rows: list[dict[str, str]],
) -> str:
    """Build a context block so the model can handle multi-page tables correctly.

    Some tables in the Birks scans span two pages. Page N shows the column
    headers (releve IDs, plot metadata) and the first batch of species rows.
    Page N+1 shows only more species rows with no headers. Without this
    context the model has no way to know which releve column each cell belongs
    to and produces bad output. Prepending this block to the prompt fixes it.
    """
    if not prev_table_row:
        return ""

    parts = ["PREVIOUS PAGE CONTEXT (read before extracting this image):"]
    table_id = prev_table_row.get("table_id", "")
    association = prev_table_row.get("association", "")
    class_ = prev_table_row.get("class", "")
    order = prev_table_row.get("order", "")
    alliance = prev_table_row.get("alliance", "")

    desc = f"table_id={table_id}"
    if association:
        desc += f", association={association}"
    if class_:
        desc += f", class={class_}"
    if order:
        desc += f", order={order}"
    if alliance:
        desc += f", alliance={alliance}"
    parts.append(f"The previous page contained: {desc}.")

    if prev_plot_rows:
        releve_ids = [p["releve_id"] for p in prev_plot_rows if p.get("releve_id")]
        parts.append(f"Releve columns from previous page (left to right): {', '.join(releve_ids)}.")
        parts.append(
            "If this image continues that table without showing column headers, "
            "use those same releve IDs for the observation data columns in this image."
        )

    parts.append(
        "If this image starts a brand-new table with its own visible headers, "
        "ignore all context above and extract fresh metadata instead."
    )
    parts.append("")
    return "\n".join(parts)


def parse_tidy_image(
    image_path: Path,
    model: str,
    prompt: str,
    max_image_side: int,
    num_predict: int,
    previous_context: str = "",
    previous_plot_rows: list[dict[str, str]] | None = None,
    num_ctx: int = 0,
    auto_rotate: bool = True,
    tile: bool = False,
    verify_counts: bool = False,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Parse one image into table rows, plot rows, and observation rows.

    Tidy mode asks the model for JSON because JSON is easier to validate than
    raw CSV when the answer contains nested data. The script then converts the
    JSON into normal CSV files.

    previous_context is prepended to the prompt so the model knows what was on
    the preceding page. This is essential for multi-page tables where column
    headers only appear on the first page.

    previous_plot_rows is used as a fallback when the model returns no plots
    (i.e. this is a continuation page with no visible column headers). Plot
    metadata — coordinates, altitude, ref_code — is inherited from the prior
    page so observation rows stay self-contained.
    """
    full_prompt = f"{previous_context}\n{prompt}" if previous_context else prompt

    if tile:
        # Tiled mode: send header tile + left/right matrix tiles separately.
        # Merge the JSON objects: use the first successful parse for metadata
        # and accumulate observations from all tiles.
        tiles = prepare_image_tiles(image_path, max_image_side, auto_rotate)
        merged: dict[str, Any] = {}
        for tile_path, cleanup_path in tiles:
            try:
                raw = call_ollama_image(
                    image_path=tile_path,
                    model=model,
                    prompt=full_prompt,
                    max_image_side=0,  # tiles are already sized
                    num_predict=num_predict,
                    response_format="json",
                    num_ctx=num_ctx,
                    auto_rotate=False,  # already rotated during tiling
                )
                obj = extract_json_object(raw)
                if not merged:
                    merged = obj
                else:
                    # Accumulate observations and plots across tiles.
                    for key in ("observations", "plots"):
                        existing = merged.get(key) or []
                        incoming = obj.get(key) or []
                        if isinstance(incoming, list):
                            seen_ids = {
                                (r.get("releve_id", ""), r.get("species", ""))
                                for r in existing
                            }
                            for r in incoming:
                                if (r.get("releve_id", ""), r.get("species", "")) not in seen_ids:
                                    existing.append(r)
                                    seen_ids.add((r.get("releve_id", ""), r.get("species", "")))
                            merged[key] = existing
            finally:
                if cleanup_path is not None:
                    cleanup_path.unlink(missing_ok=True)
        parsed = merged
    else:
        raw_response = call_ollama_image(
            image_path=image_path,
            model=model,
            prompt=full_prompt,
            max_image_side=max_image_side,
            num_predict=num_predict,
            response_format="json",
            num_ctx=num_ctx,
            auto_rotate=auto_rotate,
        )
        parsed = extract_json_object(raw_response)

    metadata = parsed.get("table_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    table_row = normalize_table(metadata, str(image_path))
    table_id = table_row["table_id"] or image_path.stem

    # Plot rows are normalized first so observation rows can inherit plot data.
    raw_plots = parsed.get("plots", [])
    if not isinstance(raw_plots, list):
        raw_plots = []
    plot_rows = [
        normalize_plot(plot, table_id, str(image_path))
        for plot in raw_plots
        if isinstance(plot, dict)
    ]

    # Continuation pages have no visible column headers, so the model returns
    # no plots. Fall back to the previous page's plots so observations still
    # inherit the correct releve IDs and coordinate metadata.
    effective_plots = plot_rows if plot_rows else (previous_plot_rows or [])
    plots_by_releve = {
        plot["releve_id"]: plot
        for plot in effective_plots
        if plot["releve_id"]
    }

    # Observation rows are long format: one species in one releve per row.
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

    # If no printed table id was found, use the image filename as a stable id.
    if not table_row["table_id"]:
        table_row["table_id"] = table_id

    # Verification pass: cross-check per-releve species counts against the
    # printed total row. On a mismatch, flag the affected observations so
    # downstream users know to check them rather than trust the count silently.
    if verify_counts and plot_rows and observation_rows:
        count_issues = verify_observation_counts(
            effective_plots if not plot_rows else plot_rows,
            observation_rows,
        )
        if count_issues:
            issue_str = "; ".join(count_issues)
            print(f"  COUNT MISMATCH: {issue_str}", flush=True)
            # Mark all observations from this image as needing review.
            for obs in observation_rows:
                if obs.get("needs_review", "").lower() != "true":
                    obs["needs_review"] = "True"
                    existing_note = obs.get("note", "")
                    mismatch_note = f"Count mismatch: {issue_str}"
                    obs["note"] = f"{existing_note}; {mismatch_note}".lstrip("; ")

    return [table_row], plot_rows, observation_rows


def parse_json_image(
    image_path: Path,
    model: str,
    keep_raw: bool,
    max_image_side: int,
    num_predict: int,
) -> dict[str, str]:
    """Run the older specimen-style parser for one image.

    This is not the current research path, but keeping it available makes it
    possible to compare against earlier tests.
    """
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
    """Run the older printed-table reconstruction parser for one image."""
    raw_response = call_ollama_image(
        image_path=image_path,
        model=model,
        prompt=prompt,
        max_image_side=max_image_side,
        num_predict=num_predict,
    )
    return parse_table_csv(raw_response)


def load_existing_rows(output_path: Path, columns: list[str]) -> pd.DataFrame:
    """Load a previous CSV, or return an empty frame with the expected columns."""
    if not output_path.exists():
        return pd.DataFrame(columns=columns)
    return pd.read_csv(output_path, dtype=str).fillna("")


def save_rows(rows: list[dict[str, str]], output_path: Path, columns: list[str]) -> None:
    """Atomically save rows to CSV in a stable column order.

    Stable column order keeps the output easy to compare in git and easy to
    read in spreadsheet tools. Writing a temporary file first prevents a crash
    during saving from leaving a half-written CSV.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[columns]
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    frame.to_csv(temporary_path, index=False)
    temporary_path.replace(output_path)


def utc_timestamp() -> str:
    """Return a timezone-aware timestamp suitable for logs and JSON files."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_tracking_rows(tracking_path: Path, resume: bool) -> list[dict[str, str]]:
    """Load the human-readable image progress tracker.

    This CSV replaces the older JSON status file and failure log. It is easier
    to review because each source image gets one simple row.
    """
    if not resume or not tracking_path.exists():
        return []
    return load_existing_rows(tracking_path, TRACKING_COLUMNS).to_dict("records")


def tracking_by_image(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """Return tracking rows keyed by image path for fast resume checks."""
    return {row["image_file"]: row for row in rows if row.get("image_file")}


def initialize_tracking_rows(
    images: list[Path],
    existing_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Make sure image_tracking.csv has one row for every source image.

    The first five images are marked successful because the current accepted
    prototype output already represents that initial reviewed batch. New images
    start as pending until the parser attempts them.
    """
    existing = tracking_by_image(existing_rows)
    initialized: list[dict[str, str]] = []
    for index, image_path in enumerate(images, start=1):
        image_file = str(image_path)
        if image_file in existing:
            row = existing[image_file]
        else:
            status = "successful" if index <= 5 else "pending"
            note = (
                "Existing first-five prototype accepted in output.csv."
                if index <= 5
                else ""
            )
            row = {
                "image_file": image_file,
                "image_number": str(index),
                "status": status,
                "last_attempt_at": "",
                "error_type": "",
                "error_message": "",
                "observations_added": "",
                "plots_detected": "",
                "tables_detected": "",
                "note": note,
            }
        for column in TRACKING_COLUMNS:
            row.setdefault(column, "")
        row["image_number"] = row.get("image_number") or str(index)
        initialized.append(row)
    return initialized


def update_tracking_row(
    rows: list[dict[str, str]],
    image_path: Path,
    *,
    status: str,
    error: Exception | None = None,
    observations_added: int | str = "",
    plots_detected: int | str = "",
    tables_detected: int | str = "",
    note: str = "",
) -> None:
    """Update one row in image_tracking.csv after an extraction attempt."""
    image_file = str(image_path)
    for row in rows:
        if row.get("image_file") == image_file:
            row["status"] = status
            row["last_attempt_at"] = utc_timestamp()
            row["error_type"] = type(error).__name__ if error else ""
            row["error_message"] = str(error) if error else ""
            row["observations_added"] = str(observations_added)
            row["plots_detected"] = str(plots_detected)
            row["tables_detected"] = str(tables_detected)
            row["note"] = note
            return


def tracking_skip_reason(row: dict[str, str], retry_failed: bool) -> str:
    """Explain why resume should skip an image, or return an empty string."""
    status = row.get("status", "")
    if status == "successful":
        return "already successful"
    if status == "unsuccessful" and not retry_failed:
        return "previously unsuccessful; use --retry-failed to retry"
    return ""


def save_tidy_outputs(
    args: argparse.Namespace,
    observation_rows: list[dict[str, str]],
    tracking_rows: list[dict[str, str]],
) -> None:
    """Save the main scientific CSV and the simple image tracker."""
    save_rows(observation_rows, args.output, OBSERVATION_COLUMNS)
    save_rows(tracking_rows, args.tracking_output, TRACKING_COLUMNS)


def print_run_summary(
    args: argparse.Namespace,
    successful: int,
    skipped: int,
    failed: int,
) -> None:
    """Print the counts and files needed to review or resume the run."""
    print("\nRun summary")
    print(f"Total images found: {args.total_images_found}")
    print(f"Processed successfully: {successful}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print(f"Main output: {args.output}")
    print(f"Image tracker: {args.tracking_output}")


def run_tidy_mode(args: argparse.Namespace, images: list[Path]) -> None:
    """Run the preferred analysis-ready extraction workflow.

    This writes one scientific CSV and one simple image tracker:
    - output/output.csv for long-format species observations with metadata
    - output/image_tracking.csv for image-level success/failure status
    """
    prompt = read_prompt(args.prompt_file)

    # Resume mode starts from the accepted output CSV and the image tracker.
    observation_rows = (
        load_existing_rows(args.output, OBSERVATION_COLUMNS).to_dict("records")
        if args.resume
        else []
    )
    tracking_rows = initialize_tracking_rows(
        args.all_images,
        load_tracking_rows(args.tracking_output, args.resume),
    )
    successful = 0
    failed = 0
    skipped = 0

    save_tidy_outputs(args, observation_rows, tracking_rows)

    # These carry column-header context across pages so multi-page tables parse
    # correctly. A table that starts on page N and continues on page N+1 only
    # shows releve IDs and plot metadata on page N, so page N+1 needs them.
    prev_table_row: dict[str, str] | None = None
    prev_plot_rows: list[dict[str, str]] = []

    for image_path in images:
        position = args.image_positions[str(image_path)]
        tracking_row = tracking_by_image(tracking_rows).get(str(image_path), {})
        reason = tracking_skip_reason(tracking_row, args.retry_failed) if args.resume else ""
        if reason:
            skipped += 1
            save_tidy_outputs(args, observation_rows, tracking_rows)
            print(f"SKIPPED: {image_path.name} - {reason}", flush=True)
            continue

        print(
            f"Processing {position}/{args.total_images_found}: {image_path.name}",
            flush=True,
        )
        try:
            # Remove this image's old rows before a retry. This prevents
            # duplicate observations if the same image is parsed again.
            image_name = str(image_path)
            observation_rows = [
                row for row in observation_rows if row.get("image_file") != image_name
            ]
            page_context = build_previous_page_context(prev_table_row, prev_plot_rows)
            image_tables, image_plots, image_observations = parse_tidy_image(
                image_path,
                args.model,
                prompt,
                args.max_image_side,
                args.num_predict,
                previous_context=page_context,
                previous_plot_rows=prev_plot_rows,
                num_ctx=args.num_ctx,
                auto_rotate=not args.no_auto_rotate,
                tile=args.tile,
                verify_counts=args.verify_counts,
            )
            observation_rows.extend(image_observations)
            successful += 1
            update_tracking_row(
                tracking_rows,
                image_path,
                status="successful",
                observations_added=len(image_observations),
                plots_detected=len(image_plots),
                tables_detected=len(image_tables),
            )
            # Carry table context forward for the next image. When a page has
            # its own column headers (image_plots non-empty) both are refreshed.
            # When it is a continuation page (no plots), keep prev_plot_rows so
            # the page after it can also inherit the column structure.
            if image_tables:
                prev_table_row = image_tables[0]
            if image_plots:
                prev_plot_rows = image_plots
            print(f"SUCCESS: {image_path.name}", flush=True)
        except Exception as error:
            failed += 1
            update_tracking_row(
                tracking_rows,
                image_path,
                status="unsuccessful",
                error=error,
            )
            print(f"FAILED: {image_path.name} - {error}", flush=True)

        # Saving after every image keeps interruption recovery simple.
        save_tidy_outputs(args, observation_rows, tracking_rows)

    save_tidy_outputs(args, observation_rows, tracking_rows)
    print_run_summary(args, successful, skipped, failed)


def main() -> None:
    """Read command-line arguments, find images, and dispatch to one mode."""
    args = build_parser().parse_args()

    # Auto-detect the strongest available model unless the user specified one.
    if args.model is None:
        args.model = detect_best_available_model()
        print(f"Auto-selected model: {args.model}", flush=True)
    else:
        print(f"Using model: {args.model}", flush=True)
    all_images = find_images(args.images_dir)
    args.all_images = all_images
    args.total_images_found = len(all_images)
    args.image_positions = {
        str(image_path): index
        for index, image_path in enumerate(all_images, start=1)
    }
    args.explicitly_skipped = all_images[: args.skip] if args.skip else []
    images = all_images
    if args.skip:
        images = images[args.skip :]
    if args.limit is not None:
        images = images[: args.limit]

    run_tidy_mode(args, images)


if __name__ == "__main__":
    main()
