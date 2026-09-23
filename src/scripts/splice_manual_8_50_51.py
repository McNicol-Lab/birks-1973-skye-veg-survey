#!/usr/bin/env python3
"""Splice hand-transcribed Table 4.8, 4.50, 4.51 rows into output/output.csv.

Does NOT run the full _build_from_vision.py pipeline (that requires a
missing gold-backup file for table 4.1 and would rewrite the whole CSV).
Instead this only:
  - removes the old junk placeholder rows for table_4_50 / table_4_51
    (every releve repeating one species, produced by a failed rotated-scan
    read), and
  - inserts freshly transcribed rows for table_4_8, table_4_50, table_4_51
    in image-number order,
leaving every other row in output.csv untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import parse_images as P  # noqa: E402
from tables_data_manual_8_50_51 import TABLES_MANUAL_8_50_51  # noqa: E402


def build_rows(tables) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for t in tables:
        image_file = t["image"]
        table_row = P.normalize_table(
            {
                "table_id": t["table_id_raw"],
                "class": t.get("class", ""),
                "order": t.get("order", ""),
                "alliance": t.get("alliance", ""),
                "association": t.get("association", ""),
                "n_releves": t.get("n_releves", ""),
                "total_species_reported": t.get("total_species", ""),
                "mean_species_per_releve": t.get("mean_species", ""),
            },
            image_file,
        )
        table_id = table_row["table_id"]

        plot_rows = [P.normalize_plot(r, table_id, image_file) for r in t["releves"]]
        plots_by_releve = {p["releve_id"]: p for p in plot_rows if p["releve_id"]}
        releve_ids = [r["releve_id"] for r in t["releves"]]

        for sp in t["species"]:
            cells = sp["cells"]
            assert len(cells) == len(releve_ids), (
                f"{table_id} {sp['name']}: {len(cells)} cells vs {len(releve_ids)} releves"
            )
            for releve_id, cell in zip(releve_ids, cells, strict=True):
                c = cell.strip()
                domin_value = raw_value = c
                obs = {
                    "releve_id": releve_id,
                    "species": sp["name"],
                    "domin_value": domin_value,
                    "raw_value": raw_value,
                    "presence_binary": "",
                    "constancy_class": sp.get("C", ""),
                    "summary_value": sp.get("D", ""),
                    "needs_review": sp.get("needs_review", True),
                    "note": sp.get("note", ""),
                }
                rows.append(P.normalize_observation(obs, table_row, plots_by_releve, image_file))
    return rows


def image_number(row: dict[str, str]) -> int:
    m = re.search(r"_(\d+)\.png$", row.get("image_file", ""))
    return int(m.group(1)) if m else 10**9


def main() -> None:
    out_path = Path("output/output.csv")
    existing = P.load_existing_rows(out_path, P.OBSERVATION_COLUMNS).to_dict("records")

    drop_ids = {"table_4_50", "table_4_51"}
    kept = [r for r in existing if r.get("table_id") not in drop_ids]
    dropped_count = len(existing) - len(kept)

    new_rows = build_rows(TABLES_MANUAL_8_50_51)

    all_rows = kept + new_rows
    all_rows.sort(key=image_number)

    P.save_rows(all_rows, out_path, P.OBSERVATION_COLUMNS)
    print(f"Dropped {dropped_count} old junk rows (table_4_50, table_4_51)")
    print(f"Added {len(new_rows)} freshly transcribed rows")
    print(f"Wrote {len(all_rows)} total rows to {out_path}")

    from collections import Counter
    counts = Counter(r["table_id"] for r in new_rows)
    for tid in sorted(counts):
        print(f"  {tid}: {counts[tid]} rows")


if __name__ == "__main__":
    main()
