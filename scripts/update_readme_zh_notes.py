#!/usr/bin/env python3
"""Update README.md with a generated list of Chinese notes."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


START_MARKER = "<!-- ZH_NOTES_LIST_START -->"
END_MARKER = "<!-- ZH_NOTES_LIST_END -->"


@dataclass(frozen=True)
class Note:
    title: str
    path: Path
    venue_year: str
    source: str
    project: str
    code: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a clear README.md table for Chinese notes in notes/."
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="README path to update. Defaults to README.md.",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=Path("notes"),
        help="Directory containing note files. Defaults to notes.",
    )
    return parser.parse_args()


def first_heading(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def metadata_value(text: str, label: str) -> str:
    match = re.search(rf"^-\s+{re.escape(label)}[：:]\s*(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def normalize_title(path: Path) -> str:
    title = path.stem.removesuffix(".zh-CN")
    return title.replace("-", " ")


def read_notes(notes_dir: Path) -> list[Note]:
    if not notes_dir.is_dir():
        raise FileNotFoundError(f"Notes directory not found: {notes_dir}")

    notes: list[Note] = []
    for path in sorted(notes_dir.glob("*.zh-CN.md")):
        text = path.read_text(encoding="utf-8")
        notes.append(
            Note(
                title=first_heading(text, normalize_title(path)),
                path=path,
                venue_year=metadata_value(text, "会议/年份"),
                source=metadata_value(text, "来源"),
                project=metadata_value(text, "项目页"),
                code=metadata_value(text, "代码"),
            )
        )
    return notes


def markdown_link(label: str, target: str) -> str:
    return f"[{label}]({target})" if target else ""


def escape_table_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def format_link_list(note: Note) -> str:
    links = [markdown_link("笔记", note.path.as_posix())]
    if note.source:
        links.append(markdown_link("来源", note.source))
    if note.project:
        links.append(markdown_link("项目", note.project))
    if note.code:
        links.append(markdown_link("代码", note.code))
    return " / ".join(links)


def render_notes_section(notes: list[Note]) -> str:
    lines = [
        START_MARKER,
        "## 中文论文笔记",
        "",
        f"共 {len(notes)} 篇中文笔记。此列表由 `python scripts/update_readme_zh_notes.py` 生成。",
        "",
        "| 论文 | 会议/年份 | 链接 |",
        "| --- | --- | --- |",
    ]

    for note in notes:
        venue_year = note.venue_year or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_table_cell(note.title),
                    escape_table_cell(venue_year),
                    escape_table_cell(format_link_list(note)),
                ]
            )
            + " |"
        )

    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def default_readme(section: str) -> str:
    return "\n".join(
        [
            "# Awesome Robot Papers",
            "",
            "Robotics paper notes and practical analysis for robot projects.",
            "",
            section,
            "",
        ]
    )


def update_readme(readme_path: Path, section: str) -> None:
    if not readme_path.exists():
        readme_path.write_text(default_readme(section), encoding="utf-8")
        return

    text = readme_path.read_text(encoding="utf-8")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)

    if start != -1 and end != -1 and start < end:
        end += len(END_MARKER)
        updated = text[:start].rstrip() + "\n\n" + section + "\n\n" + text[end:].lstrip()
    else:
        updated = text.rstrip() + "\n\n" + section + "\n"

    readme_path.write_text(updated, encoding="utf-8")


def main() -> None:
    args = parse_args()
    notes = read_notes(args.notes_dir)
    section = render_notes_section(notes)
    update_readme(args.readme, section)
    print(f"Updated {args.readme} with {len(notes)} Chinese notes.")


if __name__ == "__main__":
    main()
