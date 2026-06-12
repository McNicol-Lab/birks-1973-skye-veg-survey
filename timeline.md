# Timeline

## 1. Goal
- Build a local, offline pipeline that turns scanned Birks vegetation-table images into clean CSV data.
- The machine is an 8GB M2 MacBook Air, so the pipeline has to use smaller models, resized image copies, and one model at a time.
- Raw scans stay in `images/`.
- CSV outputs are written to `output/`.

## 2. First Plan
- The first plan was a general geo-botanical OCR pipeline.
- `parse_images.py` reads images from `images/`, sends each image to a local Ollama vision model, asks for JSON, and writes `output/output.csv`.
- The first JSON fields were `species_name`, `location`, `coordinates`, `date`, `collector`, `notes`, `other_visible_fields`, `parse_status`, `parse_error`, and `raw_response`.
- `validate_names.py` reads `output/output.csv`, checks extracted species names with a local text model, and writes `output/output_validated.csv`.
- `download_drive.py` was added as an optional helper for downloading a Google Drive image folder into `images/`.
- This plan worked as a script structure, but it assumed the scans were specimen labels. The actual images are vegetation tables, so this was not the final data shape we need.

## 3. Validator Behavior
- The validator model is `qwen2.5:3b`.
- If `species_name` is blank, the script does not call the model.
- Instead, it sets low confidence, marks `flag=true`, and writes the note `No species name was extracted.`
- If `species_name` exists, the validator asks the model to check botanical binomial format and fix obvious OCR mistakes.
- This behavior is useful later, but only after the parser extracts real taxon names from table rows.

## 4. First Ollama Model Attempt
- The originally requested vision model was `qwen2-vl:7b`.
- Ollama did not have that exact tag available.
- We pulled `qwen2.5vl:7b`, which is the available Qwen vision-language model family in Ollama.
- The parser default was temporarily pointed at `qwen2.5vl:7b`.
- This got a vision model onto the machine, but it did not give us a working pipeline yet.

## 5. First Five Image Test
- There are 96 images in `images/`.
- We tested only the first 5 images first so we could find problems without wasting time on the full set.
- Normal filename sorting would choose files like `_1`, `_10`, `_11` before `_2`.
- We changed the parser to use natural numeric sorting so the first five are `_1`, `_2`, `_3`, `_4`, `_5`.
- The first test command shape was:
  `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw`
- That first run failed for all 5 images.
- `output/output.csv` showed `parse_status=error` for each row.
- The key error was that Ollama could not find `llama-server`.

## 6. Homebrew Ollama Problem
- Homebrew installed an `ollama` command, but that install did not include the runtime binary needed for model inference.
- The missing runtime binary was `llama-server`.
- Because of that, Python could contact Ollama, but Ollama could not actually start the model.
- This was not a bug in `parse_images.py`.
- It was an Ollama installation/runtime problem.

## 7. Ollama Runtime Fix
- We installed the official Ollama macOS app bundle because it includes `llama-server`.
- The app bundle had `/Applications/Ollama.app/Contents/Resources/llama-server`.
- The first app runtime that launched was stale and reported version `0.17.0`.
- That stale runtime crashed when loading newer `qwen2.5vl` models.
- The logs showed repeated `SIGSEGV` crashes.
- A newer Ollama update zip already existed in `~/Library/Caches/ollama/updates/.../Ollama-darwin.zip`.
- We moved the stale app aside and extracted the current app bundle into `/Applications`.
- After that, Ollama reported version `0.30.7`.
- This fixed the missing-runner problem and the stale-runtime crash problem.

## 8. Full-Size Images Were Too Heavy
- The scans are roughly 2100 by 3000 pixels.
- Sending full-size scans to a local vision model was too slow on the 8GB MacBook Air.
- The 7B model was also too heavy and stalled during early tests.
- We added temporary image resizing to `parse_images.py`.
- The script leaves the original scan unchanged.
- It creates a smaller temporary JPEG, sends that to Ollama, then deletes the temporary copy.
- We tested this with `--max-image-side 1000`.

## 9. Parser Controls Added
- `--max-image-side` controls the largest side of the temporary image copy sent to Ollama.
- `--num-predict` limits how long the model response can be.
- JSON mode was added to push the model toward returning parseable JSON.
- Natural sorting was added so numbered scan files run in the expected order.
- Fresh runs now overwrite old failed test rows unless `--resume` is used.
- `--resume` still exists so interrupted long runs can skip images already processed.

## 10. Why The 7B Vision Model Was Dropped
- `qwen2.5vl:7b` was too slow for practical work on this machine.
- Even with resized images and shorter responses, it spent too long on early pages.
- We stopped stalled parser runs instead of waiting indefinitely.
- We unloaded the 7B model before trying smaller models so memory stayed under control.
- The 7B model was removed because it was not part of the working path.

## 11. Working Vision Model
- We pulled `qwen2.5vl:3b`.
- It is smaller than the 7B model and works better on the 8GB MacBook Air.
- After the Ollama runtime was fixed, `qwen2.5vl:3b` loaded and processed images.
- `parse_images.py` now defaults to `qwen2.5vl:3b`.
- Current model roles:
  `qwen2.5vl:3b` parses images.
  `qwen2.5:3b` validates extracted species names.

## 12. First Successful Parse Run
- Working command:
  `python3 parse_images.py --limit 5 --batch-size 1 --keep-raw --max-image-side 1000 --num-predict 256 --model qwen2.5vl:3b`
- The run completed in about 3 minutes 32 seconds.
- It wrote 5 rows to `output/output.csv`.
- Four rows had `parse_status=ok`.
- One row had `parse_status=error`.
- The error row failed because the model response did not contain a parseable JSON object.
- None of the first five rows produced a `species_name`.

## 13. What The First Five Results Taught Us
- The scripts can run locally after the Ollama fixes.
- The model can process resized scans on this machine.
- The first five scans appear to be vegetation-table or context pages, not specimen labels.
- That explains why the specimen-style parser did not find useful `species_name` values.
- The technical pipeline worked, but the extraction target was wrong.

## 14. First Validation Run
- We unloaded the vision model before validation so both models were not loaded at the same time.
- Validation command:
  `python3 validate_names.py --limit 5 --batch-size 1 --keep-raw`
- Since all `species_name` cells were blank, the validator skipped model calls.
- It flagged all 5 rows for review.
- `output/output_validated.csv` now has 5 validation rows.
- All 5 rows have `flag=true` and note `No species name was extracted.`
- This is correct behavior for blank names.

## 15. Current Output Meaning
- `output/output.csv` proves the parser can call Ollama, process images, and save rows.
- `output/output_validated.csv` proves the validator can read parser output and flag bad or missing names.
- These files are useful smoke-test outputs.
- They are not the final data format because the real target is table reconstruction, not one JSON record per image.

## 16. New Understanding Of The Images
- The images are structured phytosociological vegetation tables.
- They are not herbarium specimen labels.
- We should not extract one record per image with fields like collector, date, coordinates, and one `species_name`.
- We need to reconstruct the visible table as CSV.
- That means one CSV row per table row.
- Table rows can include classification rows, plot metadata rows, environmental rows, species rows, footnotes, and localities.

## 17. Table Extraction Prompt
- `csv_parsing_instructions.md` now describes the table-focused extraction target.
- It tells the model to return CSV text, not JSON.
- It uses this header:
  `row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D`
- It tells the model to preserve plot columns 1-7 plus summary columns C and D.
- It tells the model to keep dots, x marks, abundance values, abbreviated taxon names, asterisks, footnotes, and locality text.
- This prompt matches the actual Birks table images better than the original specimen-label JSON prompt.

## 18. What Worked
- The official Ollama app runtime fixed the missing `llama-server` problem.
- Updating Ollama to runtime `0.30.7` fixed the stale-runtime crashes.
- `qwen2.5vl:3b` can process resized scans locally.
- Temporary image resizing keeps the original scans untouched.
- Token limits help prevent extremely long model responses.
- Natural sorting correctly selects `_1` through `_5`.
- The parser records per-image errors instead of crashing the whole run.
- The validator correctly flags blank species names instead of pretending they are valid.

## 19. What Failed Or Was Not Good Enough
- `qwen2-vl:7b` was not available under that exact Ollama tag.
- Homebrew Ollama did not include the needed `llama-server` runtime.
- The stale Ollama app runtime crashed newer Qwen vision models.
- `qwen2.5vl:7b` was too slow and heavy for this 8GB machine.
- Full-size scans were too slow for practical local testing.
- The first JSON parser shape was wrong for these pages because it expected specimen-label fields.
- The first five parsed rows did not produce species names because the data is table-based.

## 20. Next Practical Step
- Move from printed-table reconstruction to tidy research data.
- Use the prompt in `csv_parsing_instructions.md`.
- Preferred outputs are linked CSVs: table metadata, plot/releve metadata, and long-format species observations.
- `output/output.csv` should prioritize one species-by-releve observation per row.
- Keep Domin values, presence flags, raw symbols, plot metadata, and table classification fields available for analysis.

## 21. Current Safe Command Pattern
- Current tidy parser command:
  `python3 scripts/parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 8192 --mode tidy --prompt-file prompts/csv_parsing_instructions.md`
- Tidy mode writes `output/output.csv`, `output/plots.csv`, and `output/tables.csv`.
- The older specimen-style parser is still available with `--mode json`.
- The older printed-table reconstruction path is still available with `--mode table`, but it is not the preferred research output.

## 22. First Table-CSV Batch
- Updated `instructions.md` so future parsing work points to `csv_parsing_instructions.md` and prefers table-shaped CSV over one JSON record per image.
- Updated `parse_images.py` so table mode is the default parser path.
- Table mode reads `csv_parsing_instructions.md`, sends that prompt to `qwen2.5vl:3b`, parses returned CSV rows, and saves them with the header `row_label,plot_1,plot_2,plot_3,plot_4,plot_5,plot_6,plot_7,C,D`.
- Kept old JSON mode available with `--mode json` in case we need to compare against the earlier specimen-style parser.
- First table run failed because the sandbox could not reach local Ollama at `127.0.0.1:11434`.
- Reran with local Ollama access allowed.
- The model returned useful table rows but sometimes skipped the CSV header, so the parser was loosened to keep table-shaped rows even when the header line is missing.
- Final first-five command:
  `python3 parse_images.py --limit 5 --batch-size 1 --max-image-side 1000 --num-predict 2048 --mode table --prompt-file csv_parsing_instructions.md`
- Final result: `output/output.csv` now has 150 table-shaped rows from the first 5 images and 0 parse-error rows.

## 23. Tidy Database Direction
- User clarified the desired endpoint: a modern tidy database for Birks vegetation survey data, suitable for richness, abundance, composition, functional-group, mapping, and resurvey comparisons.
- Updated `csv_parsing_instructions.md` so future extraction targets table metadata, plot/releve metadata, and long-format observations rather than a visual copy of the printed table.
- Updated `parse_images.py` so default `--mode tidy` writes linked CSV outputs.
- Tried a first-five tidy model run, but the model under-extracted badly: only 11 observations, 7 plots, 1 table, and several parse-error rows.
- Replaced that weak test output with a clean prototype generated from the user-provided table transcription.
- Current clean prototype outputs:
  `output/output.csv` has 175 long-format species-by-releve observations.
  `output/plots.csv` has 7 plot/releve metadata rows.
  `output/tables.csv` has 1 table metadata row.
- Important lesson: direct long-format extraction may need a staged process, likely printed-table extraction first and deterministic conversion to tidy tables second.

## 24. Code Explanation Comments
- Added beginner-friendly comments and docstrings to `parse_images.py`, `validate_names.py`, and `download_drive.py`.
- Explained script modes, output CSV shapes, Ollama calls, image resizing, model response parsing, resume behavior, batch saving, validation flow, and Drive downloads.
- Verified all scripts still compile with `python3 -m py_compile parse_images.py validate_names.py download_drive.py`.

## 25. Output CSV Explanation
- Reviewed `output/output.csv`, `output/plots.csv`, `output/tables.csv`, and `output/output_validated.csv`.
- Explained how each file maps to the vegetation survey project: table metadata, plot metadata, long-format species observations, and legacy validation output.

## 26. Notes And Setup Docs
- Added `docs/notes.md` with a plain-English explanation of all output CSV files and how they connect to the research project.
- Added `docs/setup.md` as the current Mac/Windows setup and run guide; future process changes should replace obsolete steps there.

## 27. Folder Structure Cleanup
- Reorganized project files into clearer folders: `scripts/` for Python scripts, `prompts/` for model prompts, and `docs/` for human-readable notes/setup.
- Kept `images/` for ignored raw scans, `output/` for tracked CSVs, and root-level `instructions.md`/`timeline.md` for agent workflow.
- Updated current commands and docs to use `scripts/parse_images.py` and `prompts/csv_parsing_instructions.md`.
