#!/usr/bin/env python3
"""Apply scripts/reparse_corrections.py to output/output.csv.

These corrections come from directly reading the source page scans in
images/ (vision, not ollama) for every table that had a flagged/blanked
coordinate after scripts/coord_fix.py. Several tables turned out to have
metadata (ref_code / map_reference / altitude / aspect / slope) that had been
mixed up with a *different* table's continuation page during the original
transcription — e.g. table_4_35's second page had picked up ref codes that
actually belong to table_4_38. Overwriting the plot metadata directly from
the scan fixes both the flagged rows and this cross-table contamination.

After overwriting, needs_review/note for the coordinate-caused flag are
cleared on any row whose corrected coordinate now resolves (checked
separately by scripts/coord_audit.py after this runs).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parse_images as P  # noqa: E402
from reparse_corrections import CORRECTIONS  # noqa: E402

CSV_PATH = Path("output/output.csv")
COORD_NOTE_MARKERS = [
    "cleared rather than guessed",
    "propagated from a trusted row sharing the same ref_code",
]


def main() -> None:
    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False, low_memory=False)

    fixed_rows = 0
    for (table_id, releve_id), (ref, mapref, alt, asp, slope) in CORRECTIONS.items():
        mask = (df["table_id"] == table_id) & (df["releve_id"] == releve_id)
        n = mask.sum()
        if n == 0:
            continue

        os_grid_square = "NG"
        map_digits = P.normalize_map_reference(mapref)
        os_grid_ref = P.build_os_grid_reference(os_grid_square, map_digits)
        easting, northing = P.os_grid_to_easting_northing(os_grid_square, map_digits)
        lat, lon = P.osgb36_to_wgs84(easting, northing)

        df.loc[mask, "ref_code"] = ref
        df.loc[mask, "map_reference"] = map_digits
        df.loc[mask, "os_grid_square"] = os_grid_square
        df.loc[mask, "os_grid_reference"] = os_grid_ref
        df.loc[mask, "easting"] = easting
        df.loc[mask, "northing"] = northing
        df.loc[mask, "latitude"] = lat
        df.loc[mask, "longitude"] = lon
        df.loc[mask, "altitude_ft"] = str(alt)
        df.loc[mask, "aspect_deg"] = str(asp)
        df.loc[mask, "slope_deg"] = str(slope)

        # Strip the earlier "coordinate cleared/propagated" note+flag now that
        # we have a real, scan-verified value; keep any other genuine note.
        for idx in df.index[mask]:
            note = df.at[idx, "note"]
            for marker in COORD_NOTE_MARKERS:
                if marker in note:
                    # remove the coordinate-specific sentence, keep the rest
                    parts = [p.strip() for p in note.split(".") if marker not in p]
                    note = ". ".join(p for p in parts if p).strip()
                    if note and not note.endswith("."):
                        note += "."
            df.at[idx, "note"] = note
            if not note or note == ".":
                df.at[idx, "needs_review"] = "false"
                df.at[idx, "note"] = ""
        fixed_rows += n

    df.to_csv(CSV_PATH, index=False)
    print(f"Applied corrections to {fixed_rows} rows across {len(set(k[0] for k in CORRECTIONS))} tables")


if __name__ == "__main__":
    main()
