#!/usr/bin/env python3
"""Download a Google Drive folder into ./images with gdown.

The image scans are intentionally kept out of git, but this helper makes it
easy to refill the local images/ folder from a shared Google Drive folder.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import gdown


# Raw scans go into images/. That folder is ignored by git.
DEFAULT_OUTPUT_DIR = Path("images")


def build_parser() -> argparse.ArgumentParser:
    """Define command-line options for the downloader."""
    parser = argparse.ArgumentParser(
        description="Download a Google Drive image folder into the local images directory."
    )

    # --url can be provided in the command. If it is missing, main() asks for it.
    parser.add_argument("--url", default=None)

    # --output lets us change the destination, but images/ is the normal target.
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR)

    # gdown's remaining_ok flag lets partially inaccessible folders continue.
    parser.add_argument("--remaining-ok", action="store_true")
    return parser


def main() -> None:
    """Ask for a Drive link if needed, then download the folder."""
    args = build_parser().parse_args()
    url = args.url or input("Google Drive folder link: ").strip()
    if not url:
        raise ValueError("A Google Drive folder link is required.")

    # Create images/ before downloading so gdown has a valid destination.
    args.output.mkdir(parents=True, exist_ok=True)

    # gdown handles the Drive folder traversal and file downloads.
    downloaded = gdown.download_folder(
        url=url,
        output=str(args.output),
        quiet=False,
        remaining_ok=args.remaining_ok,
    )
    print(f"Downloaded {len(downloaded or [])} files into {args.output}.")


if __name__ == "__main__":
    main()
