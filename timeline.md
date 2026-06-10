# Timeline

## Project operating rules
- Goal: build a local/offline pipeline that turns geo-botanical scan images into tracked CSV files.
- Machine target: MacBook Air 15-inch, M2, 8GB unified memory; this matters because large local vision models can exhaust memory or run very slowly.
- Runtime stack: Ollama locally, Python scripts, `ollama`, `pandas`, `pillow`, `tqdm`, and `gdown`.
- Git rule: work happens on `pipeline-setup`; never push directly to `main`.
- Data rule: raw scans stay in ignored `images/`; CSV outputs stay tracked in `output/`.
- Memory rule: do not run parser and validator models at the same time.

## Initial repository setup
- Created the local pipeline files: `parse_images.py`, `validate_names.py`, `download_drive.py`, `requirements.txt`, starter output CSVs, `.gitignore`, README updates, and timeline tracking.
- `parse_images.py` was built to scan `images/`, send each image to an Ollama vision model, request a strict JSON object, normalize values, and write `output/output.csv`.
- `validate_names.py` was built to read `output/output.csv`, validate extracted species names with a local text model, add `corrected_name`, `confidence`, `flag`, and `note`, and write `output/output_validated.csv`.
- `download_drive.py` was added as an optional helper that downloads a Google Drive folder into ignored `images/`.
- `.gitignore` was set to ignore raw image folders/extensions, zip archives, caches, `.env`, `.DS_Store`, and local agent instruction files.
- Verified script syntax with `python3 -m py_compile parse_images.py validate_names.py download_drive.py`.
- Ran zero-row dry runs so the scripts could be checked without loading Ollama models.
- Committed as `17f2b8a Add local botany digitizer pipeline`.

## Local instruction file handling
- User asked to keep local Codex/Claude instruction markdown files out of git.
- Updated `.gitignore` to ignore `instructions.md`, `CLAUDE.md`, `codex.md`, `codex-instructions.md`, `claude-instructions.md`, and wildcard Codex/Claude instruction filenames.
- Ran `git rm --cached instructions.md` so the file stays local for Codex to read but is removed from GitHub tracking.
- Result: `instructions.md` remains available locally, but it is no longer committed.
- Committed as `9c51e79 Ignore local agent instruction files`.

## First Ollama install attempt
- Installed Ollama with Homebrew and started it as a background service.
- Tried to pull `qwen2-vl:7b` because that was the originally requested parsing model name.
- Ollama did not publish that exact tag, so the available equivalent family model `qwen2.5vl:7b` was pulled instead.
- Updated `parse_images.py` and README so the parser default matched the installed model at that time.
- Added `*.zip` to `.gitignore` so raw image archives would not be committed.
- Verified `ollama list` showed `qwen2.5vl:7b`.
- Verified script syntax again with `python3 -m py_compile ...`.
- Committed as `af6c7ba Set up Ollama parsing model`.

## First five image test: setup and failures
- User had 96 images in `images/` and asked to run the model on the first 5.
- Found that normal lexicographic sorting would choose `_1`, `_10`, `_11`, etc., so `parse_images.py` was changed to use natural numeric sorting.
- Natural sorting means `_1`, `_2`, `_3`, `_4`, `_5` are treated as the first five images.
- First parser run used `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw`.
- That run failed for all 5 rows because the Homebrew Ollama install could not find `llama-server`.
- Error found in `output/output.csv`: `llama-server binary not found`.
- Investigated the Homebrew install and found the Homebrew keg contained only the Ollama CLI, not the runtime binary the server was trying to launch.

## Ollama runtime repair
- Installed the official Ollama macOS app bundle because it includes the missing `llama-server`.
- Launched Ollama from `/Applications/Ollama.app`.
- Confirmed the app bundle contained `/Applications/Ollama.app/Contents/Resources/llama-server`.
- Discovered the app initially launched an old/stale runtime: the bundled `ollama` reported `0.17.0`.
- The stale runtime crashed when trying to load newer `qwen2.5vl` models, producing repeated `SIGSEGV` failures in `~/.ollama/logs/server.log`.
- Found Ollama had downloaded a newer update zip into `~/Library/Caches/ollama/updates/.../Ollama-darwin.zip`.
- Moved the stale app aside as `/Applications/Ollama-0.17-backup.app`.
- Extracted the downloaded current app bundle into `/Applications`.
- Confirmed the repaired app runtime reported client version `0.30.7`.
- Confirmed the current runtime saw local models with `ollama list`.

## Parser performance fixes for 8GB RAM
- Full images were about 2100x3000 pixels, which was too heavy for first-pass local vision parsing.
- Added `--max-image-side` to `parse_images.py`.
- What it does: opens the original scan, creates a temporary resized JPEG if the scan is too large, sends that temporary copy to Ollama, then deletes the temporary file.
- Original images in `images/` are never modified.
- Added `--num-predict` to cap how many tokens Ollama can generate per image.
- What it does: prevents a full-page scan from causing the model to produce a very long answer.
- Added `format="json"` to the Ollama request so the server pushes the model toward JSON output.
- Changed non-resume behavior so running without `--resume` starts a fresh CSV instead of appending duplicates to old failed rows.
- Kept `--resume` behavior for interrupted long runs: load existing rows and skip completed images.

## 7B model was not practical on this Mac
- Tried running `qwen2.5vl:7b` after the runtime repair.
- Even with resizing and token caps, the 7B model was too slow for these page scans on the 8GB MacBook Air.
- Stopped stalled parser processes after they spent minutes without completing the first fresh image.
- Unloaded the 7B model before trying a smaller model so both models were not active at once.
- Decision: keep the 7B model only temporarily for comparison, but switch the working parser default to `qwen2.5vl:3b`.

## Working parser model: qwen2.5vl:3b
- Pulled `qwen2.5vl:3b`, a smaller local vision model in the same family.
- First attempt with the stale Ollama runtime failed quickly with `model failed to load`.
- Server logs showed the stale runtime was crashing with `SIGSEGV`.
- After replacing the app runtime with Ollama `0.30.7`, `qwen2.5vl:3b` loaded and ran.
- Updated `parse_images.py` default model to `qwen2.5vl:3b`.
- Updated README to document `qwen2.5vl:3b` as the working default for this 8GB machine.
- Removed README instructions that suggested the heavier 7B model as the normal path.

## First successful first-five parse
- Ran:
  `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw --max-image-side 1000 --num-predict 256 --model qwen2.5vl:3b`
- Result: run completed in about 3 minutes 32 seconds.
- Wrote 5 rows to `output/output.csv`.
- Parse status summary: 4 rows `ok`, 1 row `error`.
- The error row was a JSON extraction failure: the model response did not contain a parseable JSON object.
- No `species_name` values were extracted from these first 5 pages.
- Observed reason: the first pages appear to be context/table pages rather than clean specimen-name rows.

## Validation pass on first five rows
- Unloaded the vision model before running validation.
- Ran:
  `python3 validate_names.py --limit 5 --batch-size 1 --keep-raw`
- Because all 5 rows had blank `species_name`, the validator script did not need to call the text model.
- It marked each row as low-confidence, `flag=true`, with note `No species name was extracted.`
- Wrote 5 rows to `output/output_validated.csv`.
- Validation status summary: all 5 rows `ok`.
- This is expected behavior for blank species names: the script flags them for human review instead of pretending they are valid.

## Validator model setup
- Pulled the local text model `qwen2.5:3b` for future species-name validation.
- Purpose: when later image pages produce actual species names, `validate_names.py` can use this model to check binomial format and fix obvious OCR errors.
- Confirmed installed active models were `qwen2.5vl:3b` for image parsing and `qwen2.5:3b` for text validation.

## Unused model cleanup
- Removed unused local model `qwen2.5vl:7b`.
- Reason: it was too heavy/slow for this 8GB MacBook Air and is no longer the documented default.
- Kept only the active pipeline models:
  `qwen2.5vl:3b`
  `qwen2.5:3b`
- Updated README so it no longer tells the user to pull or run the removed 7B model.
- Committed as `760ae8b Remove unused Ollama model`.

## Current script behavior
- `parse_images.py` default model: `qwen2.5vl:3b`.
- Parser supports:
  `--limit` for testing a small number of images.
  `--batch-size` for periodic CSV saves.
  `--resume` for continuing a run without reprocessing completed files.
  `--keep-raw` for saving raw model output in the CSV.
  `--max-image-side` for temporary image resizing.
  `--num-predict` for response length control.
- `validate_names.py` default model: `qwen2.5:3b`.
- Validator skips model calls when `species_name` is blank and directly flags those rows.
- `download_drive.py` remains optional for importing Drive images into ignored `images/`.

## Current output state
- `output/output.csv` currently contains the first 5 parsed rows from the smoke test.
- `output/output.csv` has 4 `ok` parse rows and 1 parse error row.
- `output/output_validated.csv` currently contains the matching first 5 validation rows.
- All 5 validation rows are flagged because no species names were extracted from the first pages.
- These CSVs are intentionally tracked and pushed to GitHub.

## Important extraction direction change
- A new prompt note exists in `csv_parsing.md`.
- It clarifies that these scans are structured ecological vegetation tables, not herbarium/specimen labels.
- That means the current parser fields (`species_name`, `location`, `coordinates`, `collector`, etc.) are not the right final shape for the table images.
- The prompt in `csv_parsing.md` asks the model to reconstruct each table as CSV with rows like `Class`, `Order`, `Alliance`, `Reference Number`, environmental rows, species rows, footnotes, and locality rows.
- The required table-style header in that prompt is:
  `row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D`
- Next likely pipeline improvement: update or add a parser mode that extracts one row per table row instead of one row per image.

## GitHub workflow completed
- All commits were made on `pipeline-setup`.
- Pushed to `origin pipeline-setup`; `main` was not pushed directly.
- Important commits:
  `17f2b8a` scaffolded the pipeline.
  `9c51e79` ignored local agent instruction files.
  `af6c7ba` installed/recorded the first parsing model setup.
  `2cf51bd` recorded the first-five parse work.
  `760ae8b` removed the unused 7B model.
  `3bed950` added operating notes.

## Timeline rewrite
- Replaced the vague short timeline with a detailed handoff log.
- Included what was tried, what failed, what was changed, what commands mattered, current models, current CSV state, current table-extraction direction, and current git workflow.
