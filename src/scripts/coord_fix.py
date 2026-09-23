#!/usr/bin/env python3
"""Steps 2 and 3 of docs/reparse_plan.md.

Step 2 — cross-table ref_code propagation: if a ref_code has at least one
row elsewhere in the dataset whose coordinate passes the Skye polygon check
(scripts/coord_audit.py), copy that trusted coordinate/map-reference onto
every row for the same ref_code whose own coordinate failed the check.

Step 3 — blank rather than fabricate: any row that still fails the check
after Step 2 (no trusted value exists anywhere for that ref_code) has its
map_reference/os_grid_reference/easting/northing/latitude/longitude cleared
and needs_review set, with a note. No coordinate is invented.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from shapely.geometry import Point, shape
from shapely.ops import unary_union

GEOJSON_PATH = Path("data/skye_boundary.geojson")
CSV_PATH = Path("output/output.csv")

COORD_FIELDS = [
    "map_reference", "os_grid_square", "os_grid_reference",
    "easting", "northing", "latitude", "longitude",
]

PROPAGATE_NOTE = "Coordinate propagated from a trusted row sharing the same ref_code (map reference was missing/off-Skye on this row)."
BLANK_NOTE = "Map reference produced an off-Skye coordinate and no trusted cross-table value exists for this ref_code; coordinate fields cleared rather than guessed."


def load_skye_polygon():
    data = json.loads(GEOJSON_PATH.read_text())
    geom = shape(data["features"][0]["geometry"])
    return unary_union(geom).buffer(0.02)


def on_skye_mask(df: pd.DataFrame, skye) -> pd.Series:
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    has_coord = lat.notna() & lon.notna()
    result = pd.Series(False, index=df.index)
    for idx in df.index[has_coord]:
        result.loc[idx] = skye.contains(Point(lon.loc[idx], lat.loc[idx]))
    return has_coord, result


def main() -> None:
    skye = load_skye_polygon()
    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False, low_memory=False)

    has_coord, on_skye = on_skye_mask(df, skye)
    bad = has_coord & ~on_skye
    print(f"Rows starting off-Skye: {bad.sum()}")

    # Build trust lookup: ref_code -> first trusted coordinate row's fields.
    df["_rc"] = df["ref_code"].str.strip().str.replace(" ", "-", regex=False)
    trusted_rows = df[on_skye & df["_rc"].ne("")]
    trust_lookup = (
        trusted_rows.drop_duplicates("_rc").set_index("_rc")[COORD_FIELDS].to_dict("index")
    )
    print(f"Distinct trusted ref_codes available for propagation: {len(trust_lookup)}")

    propagated = 0
    blanked = 0
    for idx in df.index[bad]:
        rc = df.at[idx, "_rc"]
        if rc and rc in trust_lookup:
            for field, value in trust_lookup[rc].items():
                df.at[idx, field] = value
            existing_note = df.at[idx, "note"].strip()
            df.at[idx, "note"] = (existing_note + " " if existing_note else "") + PROPAGATE_NOTE
            propagated += 1
        else:
            for field in COORD_FIELDS:
                df.at[idx, field] = ""
            df.at[idx, "needs_review"] = "true"
            existing_note = df.at[idx, "note"].strip()
            df.at[idx, "note"] = (existing_note + " " if existing_note else "") + BLANK_NOTE
            blanked += 1

    df = df.drop(columns=["_rc"])
    df.to_csv(CSV_PATH, index=False)

    print(f"Propagated trusted coordinates onto {propagated} rows")
    print(f"Blanked (N/A) coordinates on {blanked} rows (needs_review set)")


if __name__ == "__main__":
    main()
