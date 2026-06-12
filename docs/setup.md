# Setup

This file explains the current working setup for the local offline vegetation-table digitizing pipeline.

Keep this file current. When the process changes, remove the old process from this file and replace it with the new successful process.

## What This Project Does

The pipeline converts scanned Birks vegetation survey tables into tidy CSV files.

The current target output is not a visual copy of the printed table. The target is analysis-ready research data:

- `output/output.csv`: long-format species observations.
- `output/plots.csv`: plot/releve metadata.
- `output/tables.csv`: table-level metadata.

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

## Required Tools

Install these first:

- Git
- Python 3.10 or newer
- Ollama
- VS Code or another editor

Ollama runs the local AI models. Python runs the pipeline scripts.

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

If Windows blocks activation, run this in PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

## Install And Start Ollama

Install Ollama from:

```text
https://ollama.com
```

After installing, start Ollama.

On Mac, open the Ollama app.

On Windows, open the Ollama app or start it from the Start menu.

Check that Ollama is running:

```bash
ollama list
```

If this command cannot connect, Ollama is not running yet.

## Pull The Local Models

The current working models are:

- `qwen2.5vl:3b` for image parsing.
- `qwen2.5:3b` for text/name validation.

Pull them once:

```bash
ollama pull qwen2.5vl:3b
ollama pull qwen2.5:3b
```

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
.jpg
.jpeg
.png
.tif
.tiff
```

The `images/` folder is ignored by git. Do not commit raw scans.

## Current Preferred Parse Command

Run a small test first:

```bash
python3 scripts/parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md
```

On Windows, if `python3` does not work, use:

```powershell
py scripts/parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md
```

What this command does:

- Reads the first 5 images from `images/`.
- Uses natural numeric sorting so image 2 comes before image 10.
- Sends one image at a time to `qwen2.5vl:3b`.
- Uses `prompts/csv_parsing_instructions.md` as the extraction prompt.
- Resizes a temporary copy of large images to a maximum side of 1000 pixels.
- Allows a longer model response with `--num-predict 8192`.
- Writes tidy CSV outputs.

## Output Files

After a successful tidy run, check:

```text
output/output.csv
output/plots.csv
output/tables.csv
```

### `output/output.csv`

Main observation table.

One row means:

```text
one species in one plot/releve
```

Use this for:

- species richness
- abundance summaries
- community composition
- ordination
- beta-diversity
- resurvey comparisons

### `output/plots.csv`

Plot/releve metadata.

One row means:

```text
one plot/releve
```

Use this for:

- map references
- altitude
- aspect
- slope
- cover
- plot size

### `output/tables.csv`

Table-level metadata.

One row means:

```text
one vegetation table or association
```

Use this for:

- class
- order
- alliance
- association
- number of releves
- reported total species count

## Validation Status

`scripts/validate_names.py` currently belongs to the older specimen-name workflow.

The older validation command is:

```bash
python3 scripts/validate_names.py --resume --batch-size 50
```

But the preferred tidy output stores species names in:

```text
output/output.csv -> species
```

So future validation should be redesigned to validate the `species` column in `output/output.csv`.

## Optional Google Drive Download

If you have a Google Drive folder link for raw images, run:

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
4. Run a small `--limit 5` test.
5. Inspect `output/output.csv`, `output/plots.csv`, and `output/tables.csv`.
6. Fix prompts or code if the output is wrong.
7. Only then run a larger batch.

## Common Problems

### Ollama Cannot Connect

Problem:

```text
Failed to connect to Ollama
```

Fix:

- Open the Ollama app.
- Run `ollama list`.
- Try the parser again.

### Model Not Found

Problem:

```text
model not found
```

Fix:

```bash
ollama pull qwen2.5vl:3b
```

### Output Has Too Few Rows

This usually means the model under-extracted the table.

For a table with 25 species and 7 releves, the observation output should have about:

```text
25 x 7 = 175 rows
```

If the output is much smaller, the prompt or extraction strategy needs work.

### Mac Is Slow Or Runs Out Of Memory

Use:

```bash
--batch-size 1 --max-image-side 1000
```

Do not run the vision parser and validation model at the same time on an 8GB machine.

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
git add .
git commit -m "short description"
git push origin pipeline-setup
```

This uploads work to the active branch without changing `main`.
