# Setup

This file explains the current working setup for the local offline vegetation-table digitizing pipeline.

Keep this file current. When the process changes, remove the old process from this file and replace it with the new successful process.

## What This Project Does

The pipeline converts scanned Birks vegetation survey tables into tidy CSV files.

The current target output is analysis-ready research data:

- `output/output.csv`: long-format species observations, one row per species per releve.
- `output/image_tracking.csv`: per-image extraction status (successful / pending / unsuccessful).

## How Accuracy Is Achieved

The pipeline uses several techniques to read these dense 1970s phytosociological tables reliably:

- **Auto-model selection.** At startup the script checks `ollama list` and picks the strongest available Qwen2.5-VL model. Larger models read fine print, rotated text, and crowded columns significantly better than the 3B model.
- **Auto-rotation.** Pages in landscape orientation (e.g. Table 4.8) are rotated to portrait before being sent to the model, so column headers appear at the top where the model expects them.
- **Full-resolution input.** By default images are sent at their original scan resolution (no downscaling). You can limit resolution with `--max-image-side` only if you are RAM-constrained.
- **Large context window.** `--num-ctx 32768` ensures dense tables are never silently truncated. The old 4096-token default made large tables appear as failed reads.
- **Temperature 0.** Deterministic model output; no hallucinated cells.
- **Multi-page context.** When a table spans two pages, the column headers from page N are carried forward so page N+1 observations inherit the correct releve IDs and coordinates.
- **Optional tiling** (`--tile`). For pages with more than ~10 releve columns, tiling sends an upscaled header tile and two upscaled matrix tiles separately, improving small-print accuracy.
- **Optional count verification** (`--verify-counts`). After extraction, per-releve species counts are cross-checked against the printed Total-number-of-species row. Any divergence of more than 2 species sets `needs_review=True` on affected rows.

## Current Folder Structure

```text
scripts/
  Python scripts that run the pipeline.

prompts/
  Model prompt files that tell Ollama what to extract.

docs/
  Human-readable setup notes, explanations, and project notes.

images/
  Raw local scan images. This folder is ignored by git.

output/
  CSV outputs. These files are tracked by git.

timeline.md
  Running project history.

instructions.md
  Local agent instructions. This file is ignored by git.
```

## Hardware Requirements

The pipeline is CPU + RAM bound at model load time. Disk is not a constraint (images + models).

| Model | Min RAM | Recommended RAM | Notes |
|---|---|---|---|
| `qwen2.5vl:3b` | 4 GB | 8 GB | Works on a MacBook Air; under-extracts dense tables |
| `qwen2.5vl:7b` | 8 GB | 12 GB | Good balance of speed and accuracy |
| `qwen2.5vl:32b` | 24 GB | 32 GB | Strong accuracy; slow on CPU |
| `qwen2.5vl:72b` | 48 GB | 64 GB | Best accuracy; requires a GPU or large RAM machine |
| `llama3.2-vision:90b` | 64 GB | 80 GB | Strong alternative; very large |

If RAM is limited, add `--max-image-side 1600` to the parse command to reduce image token cost.

## Required Tools

Install these first:

- Git
- Python 3.10 or newer
- Ollama (official app, not Homebrew)

> **Important:** Install Ollama from the official macOS or Windows app at `https://ollama.com`, not via Homebrew. The Homebrew package does not include the `llama-server` runtime binary and will fail to load models.

## Clone The Repository

Mac and Windows:

```bash
git clone <REPOSITORY_URL>
cd birks-1973-skye-veg-survey-sagole
git checkout pipeline-setup
```

Replace `<REPOSITORY_URL>` with the GitHub repository URL.

Use `pipeline-setup` for active work. Do not work directly on `main`.

## Create A Python Environment

### Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If Windows blocks activation, run this in PowerShell first:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

## Render The R Markdown EDA

To render:

```bash
Rscript docs/render_eda.R
```

Or knit from RStudio.

The script renders the notebook and then opens the HTML file in your default browser.

If packages are missing, install them first:

```bash
Rscript docs/install_packages.R
```

If you only want to render without opening the browser:

```bash
Rscript docs/render_eda.R --no-open
```

In VS Code, run the task `Render EDA HTML`.

## Install And Start Ollama

Install from the official site:

```text
https://ollama.com
```

After installing, start the Ollama app.

On Mac, open Ollama.app from Applications.
On Windows, open the Ollama app from the Start menu.

Check that Ollama is running:

```bash
ollama list
```

If this command cannot connect, Ollama is not running yet.

## Pull A Vision Model

The script auto-detects the strongest model you have installed. Pull the best one your machine can run:

### 72B (best accuracy, large machine required)

```bash
ollama pull qwen2.5vl:72b
```

### 32B (good accuracy, 24+ GB RAM)

```bash
ollama pull qwen2.5vl:32b
```

### 7B (good balance, 8+ GB RAM)

```bash
ollama pull qwen2.5vl:7b
```

### 3B (fallback, any machine)

```bash
ollama pull qwen2.5vl:3b
```

You only need one. The script picks the largest one you have when you run it.

Check installed models:

```bash
ollama list
```

## Add Images

Put raw scan images in:

```text
images/
```

Supported image types:

```text
.jpg  .jpeg  .png  .tif  .tiff
```

The `images/` folder is ignored by git. Do not commit raw scans.

## Current Parse Command

The script auto-selects the best available model and uses full-resolution input and a 32k context window by default.

### Three-image test (recommended first step)

```bash
python3 scripts/parse_images.py --limit 3 --resume
```

On Windows:

```powershell
py scripts/parse_images.py --limit 3 --resume
```

What this does:

- Detects the strongest available Qwen2.5-VL model automatically.
- Sends images at full scan resolution (no downscaling).
- Uses `--num-ctx 32768` so dense tables are not truncated.
- Uses `--num-predict 16384` so long table responses are not cut short.
- Sets temperature 0 (deterministic output).
- Auto-rotates landscape-orientation pages before sending.
- Saves after every image; `--resume` skips already-successful images on re-run.

### Full run

```bash
python3 scripts/parse_images.py --resume
```

Stop and restart at any time. `--resume` reads `output/image_tracking.csv` and continues without repeating completed images.

### Retry previously failed images

```bash
python3 scripts/parse_images.py --resume --retry-failed
```

### Tiled mode — for tables with many releve columns

Use `--tile` when a table has more than ~10 releve columns (e.g. Table 4.8). Tiling upscales the header and matrix regions separately for better small-print accuracy:

```bash
python3 scripts/parse_images.py --resume --tile
```

### Count verification — check species totals after extraction

Use `--verify-counts` to cross-check extracted per-releve species counts against the printed Total-number-of-species row. Mismatched rows are flagged `needs_review=True` automatically:

```bash
python3 scripts/parse_images.py --resume --verify-counts
```

### Low-RAM machine (8 GB or less)

If the model runs out of memory, cap image resolution and context:

```bash
python3 scripts/parse_images.py --resume --max-image-side 1600 --num-ctx 8192 --num-predict 6144
```

### Override the auto-selected model

```bash
python3 scripts/parse_images.py --model qwen2.5vl:7b --resume
```

## Output Files

After a successful run, check:

```text
output/output.csv
output/image_tracking.csv
```

`output.csv` is the scientific data file. `image_tracking.csv` is the progress file with one row per image.

### `output/output.csv`

Main observation table. One row = one species in one plot/releve.

Use this for:

- species richness per releve or community
- Domin-scale cover-range analysis
- community composition and ordination
- beta-diversity
- resurvey comparisons

Columns include `latitude`, `longitude` (WGS84, converted offline from British National Grid map references), `domin_value`, `domin_cover_min_pct`, `domin_cover_max_pct`, and `needs_review`.

### `output/image_tracking.csv`

Image-level progress tracker. One row = one source image.

- `successful` — extraction complete and at least one observation row was produced.
- `pending` — not yet attempted.
- `unsuccessful` — extraction failed; see `error_message` column.
- `review` — image was intentionally skipped (e.g. non-observation page such as a synoptic constancy table).

## Notes On Known Difficult Images

Some images need extra care and are documented in `output/image_tracking.csv`:

| Image | Table | Issue |
|---|---|---|
| 8 | 4.8 | Rotated landscape page, ~26 releve columns. Auto-rotation corrects the orientation but `--tile` gives better per-cell accuracy. All 676 rows marked `needs_review`. |
| 13, 17, 19, 20, 22, 24 | 4.13 etc. | Minor count discrepancies (±1 species) between visible entries and printed totals. Appear to be printing errors in the 1973 thesis. |
| 24 | 4.24 | Larger count gap in releve 5 (23 extracted vs 28 printed). |
| 31 | — | Severely damaged/illegible scan. Marked as non-observation. |
| 66 | 4.50 | Rotated landscape scan; releve metadata unreadable. Coordinates left blank. |
| 67 | 4.49 | Map Reference row resolution too low to read reliably. |
| 69 | 4.51 | Rotated landscape scan; releve metadata unreadable. Coordinates left blank. |
| 75–96 | 4.57 | Synoptic constancy table (species × community columns, not plots). Not a species-by-releve matrix; excluded from output.csv. |

## Optional Google Drive Download

If you have a Google Drive folder link for raw images:

```bash
python3 scripts/download_drive.py
```

Windows:

```powershell
py scripts/download_drive.py
```

The script asks for the Drive folder link and downloads files into `images/`.

## Recommended Work Pattern

1. Start Ollama.
2. Activate the Python environment.
3. Put images in `images/`.
4. Run `python3 scripts/parse_images.py --limit 3 --resume` as a test.
5. Inspect `output/output.csv` and `output/image_tracking.csv`.
6. If output looks correct, run `python3 scripts/parse_images.py --resume` for all images.
7. Add `--verify-counts` to flag count mismatches automatically.

## Common Problems

### Ollama Cannot Connect

Problem:

```text
Failed to connect to Ollama
```

Fix: Open the Ollama app. Run `ollama list`. Try the parser again.

### Model Not Found

Problem:

```text
model not found
```

Fix:

```bash
ollama pull qwen2.5vl:7b
```

### Output Has Too Few Rows

A table with 25 species and 7 releves should produce about 175 rows. If the output is much smaller, the most common cause is an insufficient context window. Try:

```bash
python3 scripts/parse_images.py --num-ctx 32768 --resume --retry-failed
```

For tables with many columns, also try `--tile`.

### Coordinates Are Blank

Coordinates are derived from the British National Grid map reference printed in each table header. Both the two-letter grid square (e.g. `NG`) and the six-digit numeric reference must be readable for coordinates to be generated. If a map reference is missing or illegible in the scan, the latitude/longitude columns will be blank for that releve.

### Ollama Crashes Or Runs Out Of Memory

Reduce the context window and image size:

```bash
python3 scripts/parse_images.py --num-ctx 8192 --num-predict 6144 --max-image-side 1600 --resume
```

Do not run multiple Ollama jobs at the same time on the same machine.

### Mac Is Slow

On a MacBook Air with 8 GB RAM, use the 3B model and cap resolution:

```bash
ollama pull qwen2.5vl:3b
python3 scripts/parse_images.py --model qwen2.5vl:3b --max-image-side 1600 --num-ctx 8192 --num-predict 6144 --resume
```

## Current Git Safety Rule

Work on:

```bash
pipeline-setup
```

Do not push directly to:

```bash
main
```

Normal save routine:

```bash
git add output/output.csv output/image_tracking.csv scripts/ timeline.md
git commit -m "short description"
git push origin pipeline-setup
```
