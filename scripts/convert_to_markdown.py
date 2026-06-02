#!/usr/bin/env python3
"""Convert a document to Markdown with MarkItDown."""

from __future__ import annotations

import argparse
from pathlib import Path

from markitdown import MarkItDown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF, Office, HTML, image, or other supported documents to Markdown."
    )
    parser.add_argument("input", type=Path, help="Source document path.")
    parser.add_argument("output", type=Path, help="Destination Markdown path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.is_file():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    markdown = MarkItDown().convert(str(args.input)).text_content
    args.output.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
