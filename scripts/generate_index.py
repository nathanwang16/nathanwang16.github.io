#!/usr/bin/env python3
"""Generate a styled index.md from markdown files in the repo."""

from __future__ import annotations

import argparse
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


def collect_markdown_files(root: Path) -> dict[str, list[Path]]:
    """Group markdown files by directory, skipping README and ignored paths."""
    grouped: dict[str, list[Path]] = {}

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
        if group == ".":
            group = "root"
        grouped.setdefault(group, []).append(relative)

    return grouped


def build_content(grouped: dict[str, list[Path]]) -> str:
    """Build the final markdown with inline HTML styling."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    groups = sorted(grouped.keys(), key=lambda g: (g != "root", g.lower()))

    lines: list[str] = []
    lines.append("# Nathan's Notes")
    lines.append("")
    lines.append(
        "<div style=\"max-width: 920px; margin: 0 auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.65;\">"
    )
    lines.append("")
    lines.append(
        "<p style=\"font-size: 1.05rem; color: #444; margin-top: 0;\">Simple writing space. All markdown files are discovered automatically.</p>"
    )
    lines.append("")
    lines.append("## Navigator")
    lines.append("")
    lines.append(
        "<div style=\"display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px;\">"
    )

    for group in groups:
        label = "root" if group == "root" else group
        anchor = f"section-{group.replace('/', '-')}"
        lines.append(
            f"<a href=\"#{anchor}\" style=\"text-decoration: none; padding: 6px 12px; border: 1px solid #ddd; border-radius: 999px; color: #222; font-size: 0.92rem;\">{label}</a>"
        )

    lines.append("</div>")
    lines.append("")
    lines.append("## Library")
    lines.append("")

    for group in groups:
        anchor = f"section-{group.replace('/', '-')}"
        title = "root" if group == "root" else group
        lines.append(f"<h3 id=\"{anchor}\" style=\"margin-bottom: 8px;\">{title}</h3>")
        lines.append("")
        for file_path in grouped[group]:
            lines.append(f"- [{display_name(file_path)}]({markdown_link(file_path)})")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"_Auto-generated at {now}_")
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
    grouped = collect_markdown_files(REPO_ROOT)
    content = build_content(grouped)
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    if not args.quiet:
        total = sum(len(v) for v in grouped.values())
        print(f"Updated {OUTPUT_FILE.name} with {total} entries.")


if __name__ == "__main__":
    main()
