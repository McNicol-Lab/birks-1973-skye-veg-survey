# Timeline

## Pipeline scaffold
- Added local Ollama extraction, species-name validation, optional Drive download, requirements, gitignore, and starter output CSVs.
- Parser writes `output/output.csv`; validator writes `output/output_validated.csv`; zero-row dry runs passed without loading models.

## Ignore local agent instructions
- Ignored `instructions.md` and Codex/Claude-style local instruction markdown files so private agent notes stay off GitHub.
- Removed `instructions.md` from git tracking while keeping it locally available; committed as `9c51e79`.

## Ollama parsing model setup
- Installed Ollama with Homebrew and started it as a background service.
- `qwen2-vl:7b` was unavailable, so pulled `qwen2.5vl:7b`; updated parser/docs and ignored raw zip archives.

## First five Ollama parse
- Replaced stale Ollama 0.17 app runtime with 0.30.7 after missing/old runner issues blocked inference.
- Added natural image sorting, temporary resize, JSON mode, token caps, and fresh-run overwrite behavior.
- Parsed first 5 of 96 images with `qwen2.5vl:3b`; output had 4 ok rows and 1 JSON parse error.
- Ran validation; all 5 rows were flagged because no species names were extracted from the first pages.
- Installed local models for parsing/validation; committed as `2cf51bd`.

## Ollama model cleanup
- Deleted unused local model `qwen2.5vl:7b`.
- Kept active pipeline models `qwen2.5vl:3b` and `qwen2.5:3b`.
