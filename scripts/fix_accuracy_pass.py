#!/usr/bin/env python3
"""Accuracy-cleanup pass on output/output.csv.

Fixes the four residual data-quality issues found in the transcribed dataset,
all resolved deterministically or by direct reading of the source scans (no
Ollama):

  Issue 2 - Duplicate species-plot rows (96 keys / 192 rows).
      Each affected species was transcribed as TWO partial rows that captured
      different presence marks of the same printed row (verified: 0 rows where
      the two copies disagree on a present value, 0 rows with two different
      non-blank constancy/summary values). We merge each pair into one row:
      union the presence marks, keep the non-blank constancy/mean-cover value.

  Issue 4 - Pipe-packed sub-association summaries in tables 4.47 and 4.49.
      These are two-sub-association tables. constancy_class (and, in 4.47,
      summary_value) stored both sub-association values packed as "A|B".
      Confirmed from the source scans (images 61, 67) that the printed C/D
      column pairs split at releve 7|8 for 4.47 and 6|7 for 4.49. We give each
      observation the value for the sub-association its releve belongs to.

  Issue 3 - Non-numeric compass annotations in numeric aspect/slope fields
      (tables 4.19 r4, 4.20 r4, 4.26 r10). Confirmed against the scans
      (images 19, 20, 27). The printed source marks ("o.N.", "E.", ".") are
      not degree values, so the numeric field is left blank and the raw mark
      recorded in the note. (4.19 r4 was doubly wrong: the CSV had put the
      slope annotation in aspect and invented a slope of 5.)

  Issue 1 - Missing coordinates for tables 4.50 and 4.51 (747 rows).
      The map-reference row was previously deemed unreadable because the
      parser saw the un-rotated landscape scan. Rotating images 66 and 69
      upright makes every printed 6-digit NG map reference legible. We
      transcribe them, convert NG -> WGS84 offline with the same functions the
      pipeline uses, and verify each point falls on the real Skye landmass.
      (CSV had ref_code B68-208 for 4.50 r14; the scan clearly reads B68-298.)

Run:  .venv/bin/python scripts/fix_accuracy_pass.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from shapely.geometry import Point, shape
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_images import (  # noqa: E402
    build_os_grid_reference,
    os_grid_to_easting_northing,
    osgb36_to_wgs84,
)

CSV_PATH = Path("output/output.csv")
BACKUP_PATH = Path("output/output.csv.pre_accuracy_pass.bak")
GEOJSON_PATH = Path("data/skye_boundary.geojson")

# --- Issue 4: releve -> sub-association split points (confirmed from scans) ---
SUBASSOC_SPLIT = {"table_4_47": 7, "table_4_49": 6}  # releves <= k are group A

# --- Issue 1: printed NG map references read from the rotated scans ----------
MAP_REFS_450 = {
    "1": "596267", "2": "707157", "3": "707157", "4": "707157", "5": "612121",
    "6": "750250", "7": "756251", "8": "413519", "9": "596267", "10": "707157",
    "11": "750250", "12": "703145", "13": "703145", "14": "612131",
}
MAP_REFS_451 = {
    "1": "413510", "2": "707157", "3": "707157", "4": "707157", "5": "707157",
    "6": "612121", "7": "750250", "8": "703145", "9": "703145", "10": "612121",
    "11": "750250", "12": "596267", "13": "596267",
}
# ref_code correction: 4.50 releve 14 reads B68-298 on the scan, not B68-208.
REFCODE_FIXES = {("table_4_50", "14"): "B68-298"}

COORD_NOTE = (
    "Coordinate recovered by rotating the landscape scan upright and reading "
    "the printed 6-digit NG map reference directly; converted to WGS84 offline "
    "and verified on the Skye landmass."
)


def relnum(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 10 ** 9


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if addition in existing:
        return existing
    return f"{existing} {addition}".strip()


def merge_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Issue 2: collapse each (table, releve, species) pair into one row."""
    key = df["table_id"] + "|" + df["releve_id"] + "|" + df["species"]
    dup_keys = set(key[key.duplicated(keep=False)])
    if not dup_keys:
        return df

    keep_idx: list[int] = []
    drop_idx: list[int] = []
    seen: dict[str, int] = {}
    for pos, (idx, k) in enumerate(zip(df.index, key)):
        if k not in dup_keys:
            keep_idx.append(idx)
            continue
        if k not in seen:
            seen[k] = idx
            keep_idx.append(idx)
        else:
            drop_idx.append(idx)

    for k, base_idx in seen.items():
        members = df.index[key == k]
        base = df.loc[base_idx]
        # presence: the printed row is present at a releve if any copy is.
        present = df.loc[members][df.loc[members, "presence_binary"] == "1"]
        if len(present):
            src = present.iloc[0]
            for col in ("presence_binary", "domin_value", "raw_value",
                        "domin_cover_min_pct", "domin_cover_max_pct"):
                df.at[base_idx, col] = src[col]
        # constancy / mean cover: keep the single non-blank value if present.
        for col in ("constancy_class", "summary_value"):
            vals = [v for v in df.loc[members, col] if str(v).strip()]
            if vals:
                df.at[base_idx, col] = vals[0]

    merged = df.drop(index=drop_idx)
    print(f"Issue 2: merged {len(dup_keys)} duplicate keys, "
          f"removed {len(drop_idx)} rows")
    return merged


def split_subassociation(df: pd.DataFrame) -> None:
    """Issue 4: unpack 'A|B' summaries onto the correct sub-association."""
    changed = 0
    for table_id, split in SUBASSOC_SPLIT.items():
        mask = df["table_id"] == table_id
        for col in ("constancy_class", "summary_value"):
            for idx in df.index[mask]:
                val = df.at[idx, col]
                if "|" not in str(val):
                    continue
                parts = val.split("|")
                if len(parts) != 2:
                    continue
                group_a = relnum(df.at[idx, "releve_id"]) <= split
                df.at[idx, col] = parts[0] if group_a else parts[1]
                changed += 1
    print(f"Issue 4: split {changed} pipe-packed sub-association cells")


def fix_aspect_slope(df: pd.DataFrame) -> None:
    """Issue 3: blank non-numeric aspect/slope, preserve raw mark in note."""
    fixes = [
        ("table_4_19", "4", "aspect", "slope", "o.N.",
         "Source aspect printed '.' (none/level) and slope printed 'o.N.' "
         "(non-numeric); numeric aspect_deg/slope_deg left blank."),
        ("table_4_20", "4", None, "slope", "o.N.",
         "Source slope printed 'o.N.' (non-numeric); numeric slope_deg left "
         "blank (aspect 270 retained)."),
        ("table_4_26", "10", None, "slope", "E.",
         "Source slope printed 'E.' (non-numeric); numeric slope_deg left "
         "blank."),
    ]
    for table_id, releve, clear_aspect, clear_slope, _raw, note in fixes:
        mask = (df["table_id"] == table_id) & (df["releve_id"] == releve)
        n = int(mask.sum())
        if clear_aspect:
            df.loc[mask, "aspect_deg"] = ""
        if clear_slope:
            df.loc[mask, "slope_deg"] = ""
        df.loc[mask, "note"] = df.loc[mask, "note"].apply(
            lambda existing: append_note(existing, note))
        print(f"Issue 3: cleaned {table_id} releve {releve} ({n} rows)")


def recover_coordinates(df: pd.DataFrame, skye) -> None:
    """Issue 1: fill 4.50/4.51 coords from the printed NG map references."""
    for table_id, refs in (("table_4_50", MAP_REFS_450),
                           ("table_4_51", MAP_REFS_451)):
        for releve, map_ref in refs.items():
            mask = (df["table_id"] == table_id) & (df["releve_id"] == releve)
            if not mask.any():
                continue
            easting, northing = os_grid_to_easting_northing("NG", map_ref)
            latitude, longitude = osgb36_to_wgs84(easting, northing)
            if not skye.contains(Point(float(longitude), float(latitude))):
                raise SystemExit(
                    f"{table_id} r{releve} {map_ref} is OFF Skye - aborting")
            df.loc[mask, "map_reference"] = map_ref
            df.loc[mask, "os_grid_square"] = "NG"
            df.loc[mask, "os_grid_reference"] = build_os_grid_reference("NG", map_ref)
            df.loc[mask, "easting"] = easting
            df.loc[mask, "northing"] = northing
            df.loc[mask, "latitude"] = latitude
            df.loc[mask, "longitude"] = longitude
            df.loc[mask, "note"] = df.loc[mask, "note"].apply(
                lambda existing: append_note(existing, COORD_NOTE))
    for (table_id, releve), ref in REFCODE_FIXES.items():
        mask = (df["table_id"] == table_id) & (df["releve_id"] == releve)
        df.loc[mask, "ref_code"] = ref
    filled = int(((df["table_id"].isin(["table_4_50", "table_4_51"])) &
                  (df["latitude"].str.strip() != "")).sum())
    print(f"Issue 1: coordinates now populated on {filled} rows of 4.50/4.51")


def main() -> None:
    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False, low_memory=False)
    if not BACKUP_PATH.exists():
        df.to_csv(BACKUP_PATH, index=False)
        print(f"Backup written to {BACKUP_PATH}")
    start_rows = len(df)

    skye = unary_union(
        shape(json.loads(GEOJSON_PATH.read_text())["features"][0]["geometry"])
    ).buffer(0.02)

    df = merge_duplicates(df)
    split_subassociation(df)
    fix_aspect_slope(df)
    recover_coordinates(df, skye)

    df.to_csv(CSV_PATH, index=False)
    print(f"\nRows: {start_rows} -> {len(df)}")
    print(f"Wrote {CSV_PATH}")


if __name__ == "__main__":
    main()
