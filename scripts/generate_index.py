#!/usr/bin/env python3
"""Generate index.html from markdown files in the repository."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "index.html"

IGNORED_FILES = {"index.md", "index.html"}
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
    """Build an HTML shell and render markdown content client-side."""
    if records:
        initial_path = records[0]["path"]
        initial_title = records[0]["title"]
    else:
        initial_path = ""
        initial_title = "No content"

    records_json = json.dumps(records, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nathan Wang</title>
  <style>
    :root {{
      --text: #111111;
      --muted: #6b7280;
      --line: #e5e7eb;
      --bg: #ffffff;
      --link: #0f172a;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Georgia, "Times New Roman", serif;
      line-height: 1.65;
    }}
    .wrap {{
      max-width: 760px;
      margin: 34px auto 64px;
      padding: 0 20px;
    }}
    h1 {{
      font-size: 42px;
      line-height: 1.1;
      margin: 0;
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      margin: 8px 0 18px;
      color: #374151;
      font-size: 19px;
    }}
    .topnav {{
      margin: 0 0 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line);
      white-space: nowrap;
      overflow-x: auto;
      scrollbar-width: thin;
    }}
    .topnav a {{
      color: var(--link);
      text-decoration: none;
      margin-right: 14px;
      font-size: 19px;
    }}
    .topnav a.active {{
      text-decoration: underline;
      text-underline-offset: 4px;
    }}
    .doc-title {{
      margin: 0 0 10px;
      font-size: 30px;
      line-height: 1.2;
      letter-spacing: -0.01em;
    }}
    .doc-path {{
      margin: 0 0 24px;
      color: var(--muted);
      font-size: 15px;
    }}
    article {{
      font-size: 20px;
    }}
    article h1, article h2, article h3, article h4 {{
      line-height: 1.25;
      margin-top: 1.2em;
      margin-bottom: 0.45em;
    }}
    article p, article ul, article ol, article blockquote {{
      margin: 0 0 0.9em;
    }}
    article img {{
      max-width: 100%;
      height: auto;
    }}
    article pre {{
      overflow-x: auto;
      border: 1px solid var(--line);
      padding: 12px;
      border-radius: 6px;
      font-size: 15px;
    }}
    article code {{
      font-size: 0.9em;
    }}
    .empty {{
      color: var(--muted);
      font-style: italic;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
  <div class="wrap">
    <h1>Nathan Wang</h1>
    <p class="subtitle">Simple notes and writing.</p>
    <nav id="topnav" class="topnav"></nav>
    <h2 id="doc-title" class="doc-title">{initial_title}</h2>
    <p id="doc-path" class="doc-path"></p>
    <article id="content"></article>
  </div>

  <script>
    const docs = {records_json};
    const topnav = document.getElementById("topnav");
    const content = document.getElementById("content");
    const docTitle = document.getElementById("doc-title");
    const docPath = document.getElementById("doc-path");

    function normalizeHash(hash) {{
      return decodeURIComponent((hash || "").replace(/^#/, ""));
    }}

    function setActive(path) {{
      for (const link of topnav.querySelectorAll("a")) {{
        link.classList.toggle("active", link.dataset.path === path);
      }}
    }}

    async function renderDoc(path) {{
      const doc = docs.find((item) => item.path === path);
      if (!doc) {{
        content.innerHTML = '<p class="empty">Document not found.</p>';
        docTitle.textContent = "Document not found";
        docPath.textContent = "";
        return;
      }}

      docTitle.textContent = doc.title;
      docPath.textContent = doc.directory === "root" ? "root" : doc.directory;
      setActive(path);

      try {{
        const response = await fetch(encodeURI(doc.path));
        if (!response.ok) {{
          throw new Error("Unable to load markdown file.");
        }}
        const md = await response.text();
        content.innerHTML = marked.parse(md);
      }} catch (_error) {{
        content.innerHTML = '<p class="empty">Failed to load markdown content.</p>';
      }}
    }}

    function initNav() {{
      if (!docs.length) {{
        topnav.innerHTML = '<span class="empty">No markdown documents found.</span>';
        content.innerHTML = '<p class="empty">Add markdown files to this repository.</p>';
        docTitle.textContent = "No content";
        docPath.textContent = "";
        return;
      }}

      topnav.innerHTML = docs.map((doc) =>
        `<a href="#${{encodeURIComponent(doc.path)}}" data-path="${{doc.path}}">${{doc.title}}</a>`
      ).join("");

      const requested = normalizeHash(window.location.hash);
      const initial = docs.some((d) => d.path === requested) ? requested : docs[0].path;
      if (window.location.hash !== `#${{encodeURIComponent(initial)}}`) {{
        history.replaceState(null, "", `#${{encodeURIComponent(initial)}}`);
      }}
      renderDoc(initial);
    }}

    window.addEventListener("hashchange", () => {{
      const requested = normalizeHash(window.location.hash);
      if (requested) {{
        renderDoc(requested);
      }}
    }});

    initNav();
  </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate index.html from markdown files in this repository."
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
