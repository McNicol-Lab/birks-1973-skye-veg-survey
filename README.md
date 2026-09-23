# Birks 1973 Vegetation Surveys – Chapter 4 Data Extraction

**Project**: Digitization, extraction, cleaning, and preliminary analysis of vegetation survey tables from H.J.B. Birks’ 1973 PhD thesis (Chapter 4), Isle of Skye, Scotland.
**Data Origin**: Birks, H. J. B. (1973). “Part II. The Present Flora and Vegetation of the Isle of Skye,” in Past and Present Vegetation of the Isle of Skye, (32 East 57th Street, New York, NY: Syndics of the Cambridge University Press), 11–220.
**Repository maintainers**: Gavin McNicol (PI)  
**Contributors**: Bhagyesh Sagole, Pawan Kumar (UIC CS)  


---

## Project Goal

Extract, clean, and harmonize vegetation survey data from Birks (1973) Chapter 4 tables to produce tidy, analysis-ready CSV files and perform preliminary clustering of survey sites. This dataset will support paleoecological research on Holocene vegetation patterns on Skye.

## Data Source
Tables from **Birks, H. J. B. (1973).** “Part II. The Present Flora and Vegetation of the Isle of Skye,” in Past and Present Vegetation of the Isle of Skye, (32 East 57th Street, New York, NY: Syndics of the Cambridge University Press), 11–220.

## Workflow

1. **Data Extraction** – Convert table images into structured data (CSV or Excel).
2. **Quality Control** – Identify and resolve anomalies (footnotes, symbols, merged cells, etc.).
3. **Data Cleaning** – Standardize species names, site codes, abundance values, and metadata.
4. **Harmonization & Merging** – Combine tables into consistent, tidy data frames.
5. **Export** – Produce clean `.csv` files (e.g., `survey_sites.csv`, `species_composition.csv`, `environmental_variables.csv`).
6. **Preliminary Analysis** – Clustering (e.g., hierarchical, k-means, NMDS) of vegetation survey sites.

## Local Offline Pipeline

This branch includes a local Ollama-based pipeline for converting image scans into tracked CSV files.

Current folder layout:

```text
scripts/      Python pipeline scripts
prompts/      Model extraction prompts
docs/         Human-readable setup notes and output explanations
images/       Raw local scans, ignored by git
output/       Tracked CSV outputs
```

For detailed Mac/Windows setup instructions, read `docs/setup.md`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ollama must be running before either model-backed script is started. Pull the models once:

```bash
ollama pull qwen2.5vl:3b
```

`qwen2.5vl:3b` is the default vision model for this 8GB MacBook Air because it completed the first local smoke test.

Put raw scans in `images/`. That folder and common image extensions are ignored by git.

Run a safe three-image tidy extraction test first:

```bash
python3 scripts/parse_images.py --resume --limit 3 --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md
```

This reads supported images from `images/`, sends one image at a time to `qwen2.5vl:3b`, uses `prompts/csv_parsing_instructions.md`, and writes tidy CSV outputs:

- `output/output.csv` for long-format species observations
- `output/image_tracking.csv` for one-row-per-image progress tracking

The script saves both files after every image. `--resume` skips images already
marked `successful` or `unsuccessful`, so the same command can safely be run
again after an interruption. Use `--retry-failed` when unsuccessful images
should be attempted again.

After reviewing the three-image test, process all remaining images:

```bash
python3 scripts/parse_images.py --resume --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md
```

Retry only the failed images while continuing to skip successful images:

```bash
python3 scripts/parse_images.py --resume --retry-failed --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md
```

`--max-image-side` makes a temporary resized copy for Ollama without changing the original scan. `--num-predict` caps the model response length. `--batch-size` remains accepted for compatibility, but durable runs save after every image.

Optionally download a Google Drive image folder into `images/`:

```bash
python3 scripts/download_drive.py
```
