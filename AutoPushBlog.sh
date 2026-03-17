#!/bin/bash

# NathanWeb auto-publisher:
# Watches markdown/content changes, rebuilds index.md, and pushes updates.
# Designed to be run by launchd (LaunchAgent) in silent background mode.

cd /Users/xiaoyuwang/NathanWeb || { echo "cd failed"; exit 1; }

watch_path="/Users/xiaoyuwang/NathanWeb"
exclude_pattern='(^|/)\.git/|(^|/)\.cursor/|(^|/)\.out-of-code-insights/'

/opt/homebrew/bin/fswatch -o -r --exclude "$exclude_pattern" "$watch_path" | while read -r; do
    python3 scripts/generate_index.py --quiet >/dev/null 2>&1

    if [[ -n "$(git status --porcelain)" ]]; then
        git add -A
        git commit -m "Auto-update content and index" >/dev/null 2>&1 || true
        git push >/dev/null 2>&1
    fi
done