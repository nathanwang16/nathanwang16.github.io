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
# Content folders to exclude entirely from website navigation/content.
EXCLUDED_CONTENT_DIRS = {
    "images",
    "scripts",
    "assets",
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


def directory_label(directory: str) -> str:
    """Display label for a directory in top navigation."""
    if directory == "root":
        return "Root"
    return Path(directory).name


def collect_markdown_files(root: Path) -> list[dict[str, str]]:
    """Collect markdown file metadata, skipping README and ignored paths."""
    records: list[dict[str, str]] = []

    for file_path in sorted(root.rglob("*.md"), key=lambda p: p.as_posix().lower()):
        relative = file_path.relative_to(root)
        parts = relative.parts

        parent_parts = parts[:-1]
        if any(part in IGNORED_DIRS or part.startswith(".") for part in parent_parts):
            continue
        if any(part.lower() in EXCLUDED_CONTENT_DIRS for part in parent_parts):
            continue
        if relative.name.lower() == "readme.md":
            continue
        if relative.name in IGNORED_FILES:
            continue

        group = relative.parent.as_posix()
        directory = "root" if group == "." else group
        is_directory_index = relative.stem.lower() == "directory"
        doc_title = directory_label(directory) if is_directory_index else extract_title(file_path)
        records.append(
            {
                "title": doc_title,
                "path": relative.as_posix(),
                "directory": directory,
                "nav_label": directory_label(directory),
                "nav_key": directory,
                "is_directory_index": "true" if is_directory_index else "false",
                "doc_label": "Overview" if is_directory_index else doc_title,
            }
        )

    return sorted(
        records,
        key=lambda r: (r["directory"] != "root", r["directory"].lower(), r["path"].lower()),
    )


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
  <title>Nathan on the Street</title>
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
    h1.site-title {{
      font-size: 28px;
      line-height: 1.15;
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
      cursor: pointer;
    }}
    .topnav a.active {{
      text-decoration: underline;
      text-underline-offset: 4px;
    }}
    .subnav {{
      margin: 0 0 22px;
      color: var(--muted);
      font-size: 17px;
      white-space: nowrap;
      overflow-x: auto;
      scrollbar-width: thin;
    }}
    .subnav a {{
      color: #374151;
      text-decoration: none;
      margin-right: 14px;
      cursor: pointer;
    }}
    .subnav a.active {{
      color: #111111;
      text-decoration: underline;
      text-underline-offset: 3px;
    }}
    article {{
      font-size: 20px;
      min-height: 320px;
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
    <h1 class="site-title">Nathan on the Street</h1>

    <nav id="topnav" class="topnav"></nav>
    <nav id="subnav" class="subnav"></nav>
    <article id="content"></article>
  </div>

  <script>
    const docs = {records_json};
    const topnav = document.getElementById("topnav");
    const subnav = document.getElementById("subnav");
    const content = document.getElementById("content");
    let activeDir = "";
    let activeDoc = "";

    const navMap = new Map();
    for (const doc of docs) {{
      const existing = navMap.get(doc.nav_key);
      if (!existing || doc.is_directory_index === "true") {{
        navMap.set(doc.nav_key, doc);
      }}
    }}
    const navDocs = Array.from(navMap.values());
    const docsByDir = new Map();
    for (const doc of docs) {{
      const list = docsByDir.get(doc.nav_key) || [];
      list.push(doc);
      docsByDir.set(doc.nav_key, list);
    }}

    function setActive(dirKey, docPath) {{
      for (const link of topnav.querySelectorAll("a")) {{
        link.classList.toggle("active", link.dataset.navKey === dirKey);
      }}
      for (const link of subnav.querySelectorAll("a")) {{
        link.classList.toggle("active", link.dataset.path === docPath);
      }}
    }}

    function preferredDocForDir(dirKey) {{
      const items = docsByDir.get(dirKey) || [];
      if (!items.length) {{
        return "";
      }}
      const directoryDoc = items.find((d) => d.is_directory_index === "true");
      return (directoryDoc || items[0]).path;
    }}

    function normalizeText(value) {{
      return value.toLowerCase().replace(/[^a-z0-9\\u4e00-\\u9fff]+/g, "");
    }}

    function stripLeadingDuplicateHeading(md, doc) {{
      const lines = md.split(/\\r?\\n/);
      let i = 0;
      while (i < lines.length && lines[i].trim() === "") {{
        i += 1;
      }}
      if (i >= lines.length) {{
        return md;
      }}
      const match = lines[i].match(/^\\s{{0,3}}#{{1,6}}\\s+(.+?)\\s*#*\\s*$/);
      if (!match) {{
        return md;
      }}
      const heading = normalizeText(match[1].trim());
      const t1 = normalizeText(doc.title);
      const t2 = normalizeText(doc.nav_label);
      if (heading !== t1 && heading !== t2) {{
        return md;
      }}
      lines.splice(i, 1);
      if (i < lines.length && lines[i].trim() === "") {{
        lines.splice(i, 1);
      }}
      return lines.join("\\n");
    }}

    function parseStateFromHash() {{
      const hash = (window.location.hash || "").replace(/^#/, "");
      if (!hash) {{
        return {{ dir: "", doc: "" }};
      }}
      const params = new URLSearchParams(hash);
      return {{
        dir: params.get("dir") || "",
        doc: params.get("doc") || "",
      }};
    }}

    function writeStateToHash(dirKey, docPath, replace = false) {{
      const params = new URLSearchParams();
      params.set("dir", dirKey);
      params.set("doc", docPath);
      const hash = `#${{params.toString()}}`;
      if (replace) {{
        history.replaceState(null, "", hash);
      }} else {{
        history.pushState(null, "", hash);
      }}
    }}

    function renderSubnav(dirKey, selectedDocPath) {{
      const items = docsByDir.get(dirKey) || [];
      if (!items.length) {{
        subnav.innerHTML = "";
        return;
      }}
      subnav.innerHTML = items.map((doc) =>
        `<a href="#" data-path="${{doc.path}}">${{doc.doc_label}}</a>`
      ).join(" ");

      for (const link of subnav.querySelectorAll("a")) {{
        link.addEventListener("click", (event) => {{
          event.preventDefault();
          const nextDoc = link.dataset.path;
          renderDirAndDoc(dirKey, nextDoc, false);
        }});
      }}
      setActive(dirKey, selectedDocPath);
    }}

    async function renderDoc(path, dirKey) {{
      const doc = docs.find((item) => item.path === path);
      if (!doc) {{
        content.innerHTML = '<p class="empty">Document not found.</p>';
        setActive(dirKey, path);
        return;
      }}

      setActive(dirKey, path);

      try {{
        const response = await fetch(encodeURI(doc.path));
        if (!response.ok) {{
          throw new Error("Unable to load markdown file.");
        }}
        const mdRaw = await response.text();
        const md = stripLeadingDuplicateHeading(mdRaw, doc);
        content.innerHTML = marked.parse(md);
      }} catch (_error) {{
        content.innerHTML = '<p class="empty">Failed to load markdown content.</p>';
      }}
    }}

    function renderDirAndDoc(dirKey, docPath, replaceHash) {{
      const items = docsByDir.get(dirKey) || [];
      if (!items.length) {{
        content.innerHTML = '<p class="empty">No markdown documents in this section.</p>';
        subnav.innerHTML = "";
        return;
      }}
      const resolvedDoc = items.some((d) => d.path === docPath) ? docPath : preferredDocForDir(dirKey);
      activeDir = dirKey;
      activeDoc = resolvedDoc;
      renderSubnav(activeDir, activeDoc);
      writeStateToHash(activeDir, activeDoc, replaceHash);
      renderDoc(activeDoc, activeDir);
    }}

    function initNav() {{
      if (!docs.length) {{
        topnav.innerHTML = '<span class="empty">No markdown documents found.</span>';
        content.innerHTML = '<p class="empty">Add markdown files to this repository.</p>';
        subnav.innerHTML = "";
        return;
      }}

      topnav.innerHTML = navDocs.map((doc) =>
        `<a href="#" data-path="${{doc.path}}" data-nav-key="${{doc.nav_key}}">${{doc.nav_label}}</a>`
      ).join("");

      for (const link of topnav.querySelectorAll("a")) {{
        link.addEventListener("click", (event) => {{
          event.preventDefault();
          const dirKey = link.dataset.navKey;
          renderDirAndDoc(dirKey, preferredDocForDir(dirKey), false);
        }});
      }}

      const state = parseStateFromHash();
      const initialDir = docsByDir.has(state.dir) ? state.dir : (navDocs[0]?.nav_key || "");
      const initialDoc = state.doc || preferredDocForDir(initialDir);
      renderDirAndDoc(initialDir, initialDoc, true);
    }}

    window.addEventListener("hashchange", () => {{
      const state = parseStateFromHash();
      if (!state.dir) {{
        return;
      }}
      renderDirAndDoc(state.dir, state.doc, true);
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
