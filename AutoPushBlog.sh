#!/bin/bash

# Path to your repo
cd /Users/xiaoyuwang/NathanWeb

# Watch index.md and auto-push when changed
fswatch -o index.md | while read; do
    if git status --porcelain | grep -q "index.md"; then
        git add index.md
        git commit -m "Auto-update: index.md modified"
        git push
        echo "$(date): index.md pushed"
    else
        echo "$(date): index.md changed but no git diff"
    fi
done