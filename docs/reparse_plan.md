# Reparse Plan — Coordinate Accuracy & `needs_review` Reduction

This is the working plan for taking `output/output.csv` from its current state
to as close to 98%+ verifiable accuracy as the source scans allow, without
fabricating any value. It formalizes the 5-step plan Gavin approved in
`timeline.md` (Section 49, "coordinate audit + accuracy roadmap") into concrete,
re-runnable steps with a real coastline check instead of a rough bounding box.

Rule for the whole pass: **if a value can't be verified, it becomes blank +
`needs_review=True` with a note — never a guess.** Blank is honest; a plausible
looking wrong number is not.

## 0. Baseline (measured before this pass)

- Total rows: 26,970
- `needs_review = true`: 1,398 rows (5.2%)
- Rows with any lat/lon: 25,321
- A rough bounding-box check (57.0–57.75N, -6.85 to -5.5) already showed ~1,726
  rows outside plausible Skye range — this is the starting estimate for bad
  coordinates, to be replaced by a real coastline check in Step 1.

## Step 1 — Real coastline-boundary check (not a bounding box)

- Fetch the actual Isle of Skye polygon boundary from OpenStreetMap (Nominatim),
  saved to `data/skye_boundary.geojson`. This is real published coastline data,
  not an approximation drawn from memory.
- For every row with a lat/lon, run a point-in-polygon test (`shapely`) against
  the Skye multipolygon (main landmass + the small attached islets OSM includes
  in the same boundary relation, e.g. Soay, Scalpay-adjacent skerries).
- Any point that does not fall inside any polygon is flagged `off_skye = True`.
  This catches both known failure modes from the earlier audit:
  - Fabricated map references on continuation tables (doubled/duplicated ref
    code digits standing in for a missing printed grid reference).
  - Short/transposed digit reads (4–5 digit map references, or one digit off,
    landing just offshore or on the mainland).
- Output: `output/coordinate_audit.csv` — one row per unique
  `(table_id, ref_code, map_reference)` combination with its coordinate and
  on/off-Skye verdict, for inspection.

## Step 2 — Cross-table ref_code propagation

- Birks reused the same field plots (`ref_code`, e.g. `B68-761`) across
  multiple tables — a plot surveyed for vascular plants in one table often
  reappears in an epiphyte or bryophyte table without repeating its grid
  reference.
- Build a trust lookup: for each `ref_code`, if at least one row for that code
  has a coordinate that passes the Step 1 land check, that coordinate is
  "trusted."
- For every row whose own coordinate is missing, off-Skye, or was produced
  from a suspiciously short/duplicated map reference, overwrite it with the
  trusted coordinate for that `ref_code` if one exists elsewhere in the
  dataset. Mark the row's note to say the coordinate was propagated from
  another table, but do not set `needs_review` for these (they now carry a
  verified value).

## Step 3 — Blank rather than fabricate

- For any row that fails Step 1 and has no trusted cross-table value from
  Step 2, clear `map_reference`, `os_grid_reference`, `easting`, `northing`,
  `latitude`, `longitude` to empty and set `needs_review = True` with a note
  explaining why (e.g. "map reference produces an off-Skye coordinate and no
  trusted cross-table value exists; cleared rather than guessed").
- This is the step that directly answers the "keep data N/A rather than
  hallucinate" requirement — no coordinate is invented.

## Step 4 — Re-parse the landscape-rotated source pages

Status per page (pages needing a rescan, from Section 49):

| Page | Image # | Table | Status |
|---|---|---|---|
| 81  | 8  | 4.8  | Done — real transcription added (species/C/D reliable, cells flagged) |
| 122 | 49 | 4.40 | **Not done** — 140 species × ~21 plots across 2 pages, out of scope for a single pass; flagged, not fabricated |
| 123 | 50 | 4.40 cont. | **Not done** — same table as above |
| 139 | 66 | 4.50 | Done — real transcription added |
| 142 | 69 | 4.51 | Done — real transcription added |

Table 4.40 remains the single largest source of `needs_review` rows and the
next real accuracy gain has to come from a dedicated pass on it, not from
this run.

## Step 5 — Residual manual spot-check

- After Steps 1–4, whatever `needs_review` rows remain are the genuinely
  ambiguous ones: specific cells or species names that are hard to read even
  on a clean scan (originally ~189 rows across images 44, 48, 53, 61–65,
  67–68), plus whatever Table 4.40 contributes.
- These are left flagged on purpose. They are candidates for a targeted
  manual check against the physical scan, not something a script can resolve.

## Verification after running

- Recompute: total rows, `needs_review` %, rows with a coordinate, rows whose
  coordinate passes the Skye polygon check, rows blanked in Step 3, rows
  fixed in Step 2.
- These real, measured numbers — not an aspirational target — go into
  `docs/accuracy_guide.md`.
