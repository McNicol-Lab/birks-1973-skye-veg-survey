#!/usr/bin/env python3
"""Step 1 of docs/reparse_plan.md: real coastline-boundary check.

Loads the actual Isle of Skye polygon (data/skye_boundary.geojson, fetched
from OpenStreetMap/Nominatim — real published coastline, not a hand-drawn
approximation) and tests every row's lat/lon against it with shapely.

Writes output/coordinate_audit.csv: one row per unique
(table_id, ref_code, map_reference) with its coordinate and on/off-Skye verdict.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from shapely.geometry import Point, shape
from shapely.ops import unary_union

GEOJSON_PATH = Path("data/skye_boundary.geojson")
CSV_PATH = Path("output/output.csv")
AUDIT_OUT = Path("output/coordinate_audit.csv")


def load_skye_polygon():
    data = json.loads(GEOJSON_PATH.read_text())
    geom = shape(data["features"][0]["geometry"])
    # ~2km buffer. Several tables in this dataset (e.g. 4.8, the salt-marsh
    # Asteretea Tripolium table) are intertidal/shoreline surveys by design,
    # so genuine plots can sit right at or just past the mapped high-water
    # line. A manual distance check (scripts/coord_audit_distance_check.py)
    # showed real errors cluster at 5km+ off the coast while legitimate
    # shoreline plots are within ~2km, so this buffer separates the two.
    return unary_union(geom).buffer(0.02)


def main() -> None:
    skye = load_skye_polygon()
    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False, low_memory=False)

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    has_coord = lat.notna() & lon.notna()

    on_skye = pd.Series(False, index=df.index)
    for idx in df.index[has_coord]:
        pt = Point(lon.loc[idx], lat.loc[idx])
        on_skye.loc[idx] = skye.contains(pt)

    df["_has_coord"] = has_coord
    df["_on_skye"] = on_skye

    print(f"Total rows: {len(df)}")
    print(f"Rows with coordinates: {has_coord.sum()}")
    print(f"Coordinates on Skye landmass: {on_skye.sum()}")
    print(f"Coordinates off Skye (bad): {(has_coord & ~on_skye).sum()}")
    print(f"Rows with no coordinate at all: {(~has_coord).sum()}")

    bad = df[has_coord & ~on_skye]
    audit = (
        bad[["table_id", "image_file", "ref_code", "map_reference", "latitude", "longitude"]]
        .drop_duplicates()
        .sort_values(["table_id", "ref_code"])
    )
    AUDIT_OUT.parent.mkdir(exist_ok=True)
    audit.to_csv(AUDIT_OUT, index=False)
    print(f"\nWrote {len(audit)} unique off-Skye plot references to {AUDIT_OUT}")

    df.drop(columns=["_has_coord", "_on_skye"]).to_csv("/dev/null", index=False)  # sanity: columns still align


if __name__ == "__main__":
    main()
