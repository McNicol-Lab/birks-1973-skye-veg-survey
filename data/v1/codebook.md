# Codebook — Birks (1973) Skye relevés (v1.0.0)

## Files

| File | Rows (approx.) | Description |
|------|----------------|-------------|
| `data/v1/observations.csv` | 26,799 | Long plot×taxon matrix (presences and absences) |
| `data/v1/plots.csv` | 520 | One row per `geo_releve_id` |
| `data/v1/taxa.csv` | 897 | Unique taxon names and presence counts |
| `output/output.csv` | 26,799 | Upstream extraction table (includes pipeline fields) |

Use **`data/v1/`** for analysis and citation. `output/` is retained for provenance.

## Primary key

`geo_releve_id` = `{table_id}_{releve_id}` (e.g. `table_4_1_3`).  
`releve_id` alone is only unique within a phytosociological table.

## observations.csv

| Column | Description |
|--------|-------------|
| geo_releve_id | Stable plot key |
| table_id | Source table id (e.g. `table_4_1`) |
| releve_id | Column number within the published table |
| ref_code | Birks field reference code when given (e.g. `B68-155`) |
| species | Taxon string as digitised from the table |
| domin_value | Domin abundance (1–10, `+`, `x`, …). Blank = absent in matrix |
| domin_cover_min_pct / max_pct | Approximate cover bounds mapped from Domin when available |
| presence_binary | `1` present, `0` absent in that table column |
| raw_value | Raw cell string from extraction (blank if sentinel `.` was used for absence) |
| constancy_class / summary_value | Table summary fields when present |
| image_file | Source scan filename (scans not deposited; CUP copyright) |
| needs_review | Extraction QC flag (`false` in v1.0.0 snapshot) |
| note | Free-text extraction note |

**Sentinels:** published absences encoded as `.` in the extraction CSV are blank strings here.

**Domin dots / symbols:** `+`, `x`, and similar symbols are retained as in the source tables (known limitation: not always mapped to cover %).

## plots.csv

Plot / relevé metadata collapsed to one row per `geo_releve_id` (modal non-empty value across matrix rows).

| Column | Description |
|--------|-------------|
| class, order, alliance, association | Syntaxonomic hierarchy from the table header |
| map_reference, os_grid_square, os_grid_reference | Map / OS grid as published |
| easting, northing | Projected coordinates when derived |
| latitude, longitude | WGS84 from OS grid georeferencing |
| altitude_ft / altitude_m | Sparse in source (few plots have altitude) |
| aspect_deg, slope_deg, cover_pct, plot_area_m2 | Environmental / plot descriptors when given |
| species_reported / total_species_reported | Header counts when present |

**Georeferencing:** OS National Grid references from the published tables were converted to WGS84 latitude/longitude. Some plots share coordinates when only a coarse grid reference was published. Coordinate audit tooling lives under `src/` and is not required to use the data.

**Known gaps:** altitude is sparse (~7 of 520 plots have `altitude_m` in this snapshot); Domin symbols (`+`, `x`) are retained; page images are excluded.

## taxa.csv

| Column | Description |
|--------|-------------|
| taxon_name | Unique species / taxon string |
| n_plots_present | Number of plots with `presence_binary=1` |
| n_matrix_cells | Number of long-table rows for this taxon (incl. absences) |

## Provenance (do not confuse)

- **Published source:** Birks, H. J. B. (1973). *Past and Present Vegetation of the Isle of Skye*. Cambridge University Press. Part II, present vegetation relevés.
- **Field period:** ca. 1966–1969 (present-day vegetation at the time of survey), not Holocene paleoecological reconstructions.
- **PhD thesis (1969)** is related background; the citable published tables are the 1973 CUP volume.

## License

CC BY 4.0 for the digitisation and derived fields. CUP book content and table scans are not licensed here and are not included in the DOI package.
