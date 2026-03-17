#!/usr/bin/env python3
"""Generate a styled index.md from markdown files in the repo."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "index.md"

IGNORED_FILES = {"index.md"}
IGNORED_DIRS = {
    ".git",
    ".github",
    ".vscode",
    ".idea",
    "__pycache__",
    "node_modules",
    ".cursor",
    ".out-of-code-insights",
}


def display_name(path: Path) -> str:
    """Humanize file names while preserving concise structure."""
    name = path.stem.replace("-", " ").replace("_", " ").strip()
    return name.title() if name else path.stem


def markdown_link(path: Path) -> str:
    """Create a URL-safe markdown link for GitHub Pages."""
    return quote(path.as_posix(), safe="/-_.~")


def extract_title(file_path: Path) -> str:
    """Use the first markdown heading as title fallback to filename."""
    heading_pattern = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file_path.read_text(encoding="utf-8", errors="ignore")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        match = heading_pattern.match(stripped)
        if match:
            title = match.group(1).strip()
            return title if title else display_name(file_path)

    return display_name(file_path)


def collect_markdown_files(root: Path) -> list[dict[str, str]]:
    """Collect markdown file metadata, skipping README and ignored paths."""
    records: list[dict[str, str]] = []

    for file_path in sorted(root.rglob("*.md"), key=lambda p: p.as_posix().lower()):
        relative = file_path.relative_to(root)
        parts = relative.parts

        if any(part in IGNORED_DIRS or part.startswith(".") for part in parts[:-1]):
            continue
        if relative.name.lower() == "readme.md":
            continue
        if relative.name in IGNORED_FILES:
            continue

        group = relative.parent.as_posix()
        directory = "root" if group == "." else group
        records.append(
            {
                "title": extract_title(file_path),
                "path": relative.as_posix(),
                "directory": directory,
                "anchor": "doc-" + relative.as_posix().replace("/", "-").replace(".", "-"),
            }
        )

    return records


def build_content(records: list[dict[str, str]]) -> str:
    """Build a clean, text-first page inspired by Soumith-style simplicity."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []
    lines.append("# Nathan Wang")
    lines.append("")
    lines.append("<div style=\"max-width: 760px; margin: 0 auto; font-family: Georgia, 'Times New Roman', serif; line-height: 1.65; color: #111;\">")
    lines.append("")
    lines.append("<p style=\"margin-top: 0; color: #333;\">Simple notes and writing.</p>")
    lines.append("")
    if records:
        nav_links: list[str] = []
        for record in records:
            nav_links.append(
                f"<a href=\"#{record['anchor']}\" style=\"text-decoration: none; color: #111;\">{record['title']}</a>"
            )
        lines.append("<p>" + " | ".join(nav_links) + "</p>")
    else:
        lines.append("<p><em>No markdown documents found yet.</em></p>")
    lines.append("")
    lines.append("<hr style=\"border: 0; border-top: 1px solid #e5e5e5; margin: 18px 0 22px;\">")
    lines.append("")
    lines.append("## Writing")
    lines.append("")
    for record in records:
        lines.append(f"<div id=\"{record['anchor']}\" style=\"margin-bottom: 14px;\">")
        lines.append(f"<a href=\"{markdown_link(Path(record['path']))}\" style=\"text-decoration: none; color: #111; font-size: 1.06rem;\"><strong>{record['title']}</strong></a><br>")
        lines.append(
            f"<span style=\"color: #666; font-size: 0.92rem;\">{record['directory']}</span>"
        )
        lines.append("</div>")
        lines.append("")
    lines.append("<hr style=\"border: 0; border-top: 1px solid #e5e5e5; margin: 18px 0 12px;\">")
    lines.append("")
    lines.append(f"<p style=\"color: #777; font-size: 0.9rem; margin-bottom: 0;\">Auto-generated at {now}</p>")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate index.md from markdown files in this repository."
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress non-error output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = collect_markdown_files(REPO_ROOT)
    content = build_content(records)
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    if not args.quiet:
        total = len(records)
        print(f"Updated {OUTPUT_FILE.name} with {total} entries.")


if __name__ == "__main__":
    main()
