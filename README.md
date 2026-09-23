# Digitised phytosociological relevés from Birks (1973), Isle of Skye

**Version:** 1.0.0 (Zenodo-ready snapshot)  
**Contents:** 520 plots · 897 taxa · 26,799 long-table observations  
**License:** [CC BY 4.0](LICENSE) (digitisation & derived fields only — not the CUP book or page scans)

## What this is

A tidy digitisation of **present-vegetation** phytosociological relevés published in:

> Birks, H. J. B. (1973). *Past and Present Vegetation of the Isle of Skye*. Cambridge University Press. Part II (“The Present Flora and Vegetation of the Isle of Skye”), pp. 11–220.

Field surveys were carried out around **1966–1969**. These are contemporary relevés from that period, not Holocene paleoecological reconstructions.

Original surveyor / published source: **H. J. B. Birks**. Digitisation and packaging: **Gavin McNicol**, **Bhagyesh Sagole**, **Pawan Kumar** (UIC).

## Cite this dataset

See [`CITATION.cff`](CITATION.cff). After Zenodo minting, replace the DOI placeholder in `LICENSE` / release notes with the Zenodo DOI.

Also cite the original book when using the ecological content.

## Files to use

| Path | Role |
|------|------|
| [`data/v1/observations.csv`](data/v1/observations.csv) | QC’d long plot×taxon table (`.` absences → blank) |
| [`data/v1/plots.csv`](data/v1/plots.csv) | One row per `geo_releve_id` |
| [`data/v1/taxa.csv`](data/v1/taxa.csv) | Taxon index |
| [`data/v1/codebook.md`](data/v1/codebook.md) | Column definitions & known gaps |

Upstream extraction table (provenance): `output/output.csv`.

## Georeferencing

Where OS grid references appear in the published tables, they were converted to WGS84 latitude/longitude. Coverage is incomplete at fine scale when only coarse grid references were printed. Altitude is sparse in the source tables.

## Known limitations

- Domin symbols such as `+` and `x` are retained; cover % mapping is incomplete for those cells.
- Altitude is available for only a small subset of plots.
- Table **page scans are not included** (Cambridge University Press copyright). They are not public domain.
- Syntaxonomic names and taxon strings follow the published tables (period taxonomy).

## Extraction pipeline (optional)

Code under [`src/`](src/) reproduces the digitisation workflow (local vision / parsing tools). **It is not required to use the data products in `data/v1/`.** Scans used during extraction are stored privately and must not be redistributed with a DOI package.

## Repository layout

```text
data/v1/     Citable CSV products + codebook
output/      Upstream extraction outputs (provenance)
src/         Digitization pipeline (optional)
docs/        Working notes / EDA (not part of the minimal DOI file set)
```

## Zenodo deposit note

Prefer a GitHub Release **v1.0.0** linked via the Zenodo–GitHub integration, or upload a zip limited to:

`LICENSE`, `CITATION.cff`, `README.md`, `data/v1/*`  
(and optionally a short note pointing at `src/` on GitHub).

Do not include `.vscode/`, local model notes, or page images.
