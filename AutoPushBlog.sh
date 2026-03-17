#!/bin/bash

# Log to desktop
exec >> ~/Desktop/fswatch_debug.log 2>&1

echo "Started watching at $(date)"

cd /Users/xiaoyuwang/NathanWeb || { echo "cd failed"; exit 1; }

watch_path="/Users/xiaoyuwang/NathanWeb"
exclude_pattern='(^|/)\.git/|(^|/)\.cursor/|(^|/)\.out-of-code-insights/'

/opt/homebrew/bin/fswatch -o -r --exclude "$exclude_pattern" "$watch_path" | while read -r; do
    python3 scripts/generate_index.py

    if [[ -n "$(git status --porcelain)" ]]; then
        git add -A
        git commit -m "Auto-update content and index" || true
        git push
        echo "$(date): changes committed and pushed"
    fi
done