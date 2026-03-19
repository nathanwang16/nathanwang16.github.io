#!/usr/bin/env python3
"""Run a local preview server with automatic index regeneration."""

from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import subprocess
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR_SCRIPT = REPO_ROOT / "scripts" / "generate_index.py"
WATCH_INTERVAL_SECONDS = 1.0

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


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve NathanWeb locally and auto-regenerate index.html on changes."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host interface to bind (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve on (default: 8000).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=WATCH_INTERVAL_SECONDS,
        help="Polling interval in seconds for file changes (default: 1.0).",
    )
    return parser.parse_args()


def should_ignore(path: Path) -> bool:
    relative = path.relative_to(REPO_ROOT)
    return any(part in IGNORED_DIRS or part.startswith(".") for part in relative.parts[:-1])


def watched_files() -> list[Path]:
    files = [GENERATOR_SCRIPT]
    for md_file in REPO_ROOT.rglob("*.md"):
        if should_ignore(md_file):
            continue
        files.append(md_file)
    return files


def fingerprint() -> tuple[tuple[str, int], ...]:
    snapshot: list[tuple[str, int]] = []
    for file_path in watched_files():
        try:
            stat = file_path.stat()
        except FileNotFoundError:
            continue
        snapshot.append((file_path.relative_to(REPO_ROOT).as_posix(), stat.st_mtime_ns))
    snapshot.sort()
    return tuple(snapshot)


def regenerate_index() -> bool:
    result = subprocess.run(
        ["python3", str(GENERATOR_SCRIPT), "--quiet"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("Failed to regenerate index.html")
        if result.stderr.strip():
            print(result.stderr.strip())
        return False
    return True


def watch_for_changes(interval: float, stop_event: threading.Event) -> None:
    previous = fingerprint()
    while not stop_event.is_set():
        current = fingerprint()
        if current != previous:
            if regenerate_index():
                print("Detected changes. Regenerated index.html")
            previous = current
        stop_event.wait(interval)


def main() -> None:
    args = parse_args()
    if not regenerate_index():
        raise SystemExit(1)

    # Serve files from repo root so markdown fetch paths match production layout.
    handler = http.server.SimpleHTTPRequestHandler
    stop_event = threading.Event()

    watcher_thread = threading.Thread(
        target=watch_for_changes,
        args=(args.interval, stop_event),
        daemon=True,
    )
    watcher_thread.start()

    with ReusableTCPServer((args.host, args.port), handler) as httpd:
        print(f"Local preview running at http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop.")
        try:
            # Keep serving from the repository root.
            os.chdir(REPO_ROOT)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping preview server.")
        finally:
            stop_event.set()


if __name__ == "__main__":
    main()
