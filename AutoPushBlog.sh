#!/bin/bash

# NathanWeb hourly auto-publisher (single run):
# 1) Rebuilds index.md quietly
# 2) If git detects any repo changes, commits and pushes
# 3) Exits immediately (launchd StartInterval runs it every hour)

cd /Users/xiaoyuwang/NathanWeb || { echo "cd failed"; exit 1; }

python3 scripts/generate_index.py --quiet >/dev/null 2>&1

if [[ -z "$(git status --porcelain)" ]]; then
    exit 0
fi

git add -A
git commit -m "Auto-update content and index" >/dev/null 2>&1 || exit 0
git push >/dev/null 2>&1 || true