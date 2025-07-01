#!/bin/bash

# Log to desktop
exec >> ~/Desktop/fswatch_debug.log 2>&1

echo "Started watching at $(date)"

cd /Users/xiaoyuwang/NathanWeb || { echo "cd failed"; exit 1; }

/opt/homebrew/bin/fswatch -o /Users/xiaoyuwang/NathanWeb/index.md | while read; do
    # Check if index.md has changed according to Git
    if git status --porcelain | grep -q "index.md"; then
        git add .
        git commit -m "Auto-update: index.md modified"
        git push
        echo "$(date): index.md committed and pushed"
    fi
done