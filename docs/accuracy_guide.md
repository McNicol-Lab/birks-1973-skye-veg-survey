# Accuracy Guide

This documents how `output/output.csv` was checked for accuracy, what was
fixed, and what the real (measured, not aspirational) numbers are after two
passes: the coordinate-audit pass and the direct-rescan reparse pass
(`docs/reparse_plan.md`). Every number below comes from running a script
against the actual CSV — none of it is estimated from memory.

## Two separate things this guide measures

"Accuracy" means different things for coordinates vs. for table cells, so
they're reported separately rather than blended into one misleading number.

## 1. Coordinate accuracy — verified against a real coastline

**Method:** every row's `latitude`/`longitude` was tested against the actual
Isle of Skye boundary polygon, fetched from OpenStreetMap/Nominatim
(`data/skye_boundary.geojson` — real published coastline data, not a
hand-drawn approximation) using `shapely` point-in-polygon (`scripts/coord_audit.py`).
A ~2km buffer around the coastline accounts for legitimate intertidal/shoreline
survey plots (e.g. Table 4.8's salt-marsh species) that sit right at the
high-water mark.

**Pass 1 (bounding-box era, before any fix):** only 72.4% of populated
coordinates actually fell on Skye; 75 unique field plots had a fabricated or
mistranscribed map reference, mostly on continuation pages that don't
reprint the grid reference.

**Pass 2 (direct rescan, this session):** rather than only blanking the bad
plots, every affected source page (`images/*.png`) was read directly —
by eye, not OCR/ollama — to recover the real printed Reference Number,
Map Reference, Altitude, Aspect, and Slope rows. This found the actual root
cause on several tables: continuation pages had picked up plot metadata that
belonged to a *different* table's page (e.g. Table 4.35's continuation page
had ref codes that actually belong to Table 4.38 — confirmed by reading both
tables' printed headers directly). 19 tables' releve metadata were corrected
this way (`scripts/reparse_corrections.py` + `scripts/apply_reparse_corrections.py`),
recovering **13,838 rows** with a verified-correct coordinate instead of a
blank.

**Final result (after the Section 56 accuracy-cleanup pass):**

| Metric | Value |
|---|---|
| Rows with a coordinate | 26,799 |
| Coordinates verified on real Skye land | **26,799 / 26,799 (100%)** |
| Rows with no coordinate | **0 (0%)** |

The last 747 blank rows (Tables 4.50 and 4.51) were resolved by rotating those
two landscape scans upright and reading the printed 6-digit NG map references
directly — see `timeline.md` Section 56. Every row in the dataset now carries a
coordinate verified on the Skye landmass.

Every coordinate in the file is now backed by one of: (a) a plot metadata
row read directly from the printed scan, (b) a cross-table `ref_code` match
to another table's verified-good plot, or (c) for plots where even a rescan
couldn't recover a 6-digit map reference, a real-world geocoding lookup
(OpenStreetMap/Nominatim) of the locality name Birks printed for that
releve, checked against the Skye polygon before use and disclosed as
approximate in the row's note. **Zero rows contain a coordinate known to be
wrong**, and every plot that had a confident locality match now has one
(the last holdout, Table 4.14's "Loch nan Eilean," resolved on a retry with
a Skye-bounded search).

There are no remaining blank rows. Tables 4.50 and 4.51 — the last holdouts —
were resolved not by geocoding their locality names but by rotating the
landscape scans upright, which made every printed 6-digit NG map reference
legible; the transcribed references cross-check exactly against the same grid
references already trusted in other tables.

## 2. Table-cell / transcription accuracy

| Bucket | Rows | % of dataset | What it means |
|---|---|---|---|
| **Total flagged (`needs_review=true`)** | **0** | **0.00%** | Nothing in the current dataset is marked as questionable |

**Field-level accuracy: 100%** of the 26,799 rows currently in the dataset
(`(26,799 − 0) / 26,799`). This isn't the same as "every value is certainly
right" — it means every row has either been read from a clean, legible
source, cross-verified, or removed if it couldn't be confirmed. See below
for what specifically changed to get here.

Four direct-scan passes (`timeline.md` Sections 52–55) closed the gap:

- Fixed a duplicated/mislabeled species row in Table 4.36 (17 rows deleted),
  a wrong "Rhacomitrium lanuginosum" row in Table 4.38 (including an invalid
  Domin value of "16", outside the 1–10 scale), and a completely mismatched
  "Deschampsia flexuosa" row in Table 4.43.
- Found and applied a correction for Table 4.33 that had been identified
  early in the session but never actually written to the correction file —
  708 rows recovered a real coordinate as a result. Table 4.34 got the same
  treatment for one more plot (59 rows).
- Introduced locality-name geocoding for plots where no map reference was
  ever legible: looked up the real coordinates of the printed locality name
  (e.g. "Bla Bheinn," "Meanish," "Loch nan Eilean") via OpenStreetMap/
  Nominatim, verified each one lands on the real Skye landmass, and used it
  — disclosed as approximate in the note — instead of leaving the row
  blank. 255 rows recovered this way.
- Independently re-verified Tables 4.8, 4.50, and 4.51 by reading the actual
  source images a second time (rather than relying on the separately
  supplied reference PDF used originally) and confirmed they matched the
  transcription — 1,203 rows moved from "best effort" to confirmed.
- Re-read every one of the final 72 flagged rows directly against their
  source pages (images 62–65, 67–68). Found genuine bugs, not just
  uncertainty: several rows had a constancy class literally stored as a
  merged string like `"II|III"` from a two-association table, or a row of
  all-absent cells paired with a nonzero mean cover — a contradiction.
  Re-read and corrected those against the printed page. Separately, found
  that 4 species ("Anomalodontium sp.," "Dicranodontium sp.," "P.
  atlantica," and 3 footnote species on Table 4.48) had a nonzero constancy
  class but zero presence in every single releve — checked every row of the
  relevant pages and confirmed these names don't appear anywhere in the
  printed tables at all. They were invented by the original transcription
  pass and were deleted (58 rows) rather than left flagged.

## 3. What's still outstanding

- **Table 4.40** (140 species × ~21 plots, split across 2 genuinely
  landscape-rotated page images and 4 vegetation sub-groups) still isn't in
  the dataset. Its source pages (images 49–50) were checked directly and
  confirmed to be rotated/small enough that a reliable transcription isn't
  achievable without a proper rescan.
- **Table 4.49 releve 14** (field ref `B67-102`): the upright read of image 67
  shows a 14th releve column that the original transcription dropped; the
  dataset currently holds releves 1–13 for that table. Recovering it needs its
  full species column transcribed.

## How to re-run this check

```bash
.venv/bin/python3 scripts/coord_audit.py               # report-only: counts + output/coordinate_audit.csv
.venv/bin/python3 scripts/coord_fix.py                 # Step 2 (propagate) + Step 3 (blank) — first pass
.venv/bin/python3 scripts/apply_reparse_corrections.py # applies direct-rescan corrections (scripts/reparse_corrections.py)
```

All three use `data/skye_boundary.geojson`. If that boundary file is ever
refreshed from Nominatim, re-run `coord_audit.py` to re-validate the whole
dataset against the new polygon.
