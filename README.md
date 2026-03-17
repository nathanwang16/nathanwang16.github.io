# nathanwang.github.io

Minimal personal website powered by markdown files.

## What this now does

- Uses **all markdown files recursively** in this repo as website content.
- Supports **nested folder structure**.
- Automatically **ignores any file named `README.md`**.
- Auto-generates a clean `index.md` with:
  - top "navigator bins" (directory chips)
  - grouped links to every markdown page
  - simple, elegant styling

## Files added/updated

- `scripts/generate_index.py`
  - Scans the repo for markdown files.
  - Excludes `README.md`, `index.md`, and hidden/system directories.
  - Regenerates `index.md` with a lightweight styled navigator.
- `.github/workflows/update-index.yml`
  - On push, regenerates `index.md` automatically.
  - Commits and pushes `index.md` if changed.
- `AutoPushBlog.sh`
  - Watches your repo for changes.
  - Regenerates `index.md`.
  - Auto-commits and pushes updates.

## Your ideal workflow (now supported)

1. Create/remove folders.
2. Add/edit any `.md` files.
3. Run local auto-update script or push to GitHub.
4. Website navigation/content updates automatically.

## Local auto-update usage

Make it executable once:

```bash
chmod +x AutoPushBlog.sh
```

Run:

```bash
./AutoPushBlog.sh
```

## Optional manual regenerate

```bash
python3 scripts/generate_index.py
```

## Style direction

The generated `index.md` keeps a quiet, text-first aesthetic: light typography, simple spacing, and top-level navigation chips, while staying markdown-native and easy to maintain.