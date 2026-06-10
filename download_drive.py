#!/usr/bin/env python3
"""Download a Google Drive folder into ./images with gdown."""

from __future__ import annotations

import argparse
from pathlib import Path

import gdown


DEFAULT_OUTPUT_DIR = Path("images")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download a Google Drive image folder into the local images directory."
    )
    parser.add_argument("--url", default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--remaining-ok", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    url = args.url or input("Google Drive folder link: ").strip()
    if not url:
        raise ValueError("A Google Drive folder link is required.")

    args.output.mkdir(parents=True, exist_ok=True)
    downloaded = gdown.download_folder(
        url=url,
        output=str(args.output),
        quiet=False,
        remaining_ok=args.remaining_ok,
    )
    print(f"Downloaded {len(downloaded or [])} files into {args.output}.")


if __name__ == "__main__":
    main()
