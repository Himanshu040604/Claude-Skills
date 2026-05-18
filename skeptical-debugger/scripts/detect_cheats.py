#!/usr/bin/env python3
"""Detect test/signal gaming in a unified diff.

Static text analysis only: never executes diff content or the code it describes.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from parse_diff import parse_diff

SEVERITIES = ("high", "medium", "low")


def load_catalog() -> dict:
    """Load and pre-compile the gaming-pattern catalog from cheat_patterns.json."""
    data = json.loads((Path(__file__).parent / "cheat_patterns.json").read_text())
    for pat in data["patterns"]:
        pat["compiled"] = re.compile(pat["regex"])
    data["test_file_compiled"] = [re.compile(p) for p in data["test_file_patterns"]]
    return data


def is_test_file(path: str, catalog: dict) -> bool:
    """Return True if the path matches any test-file pattern in the catalog."""
    return any(rx.search(path) for rx in catalog["test_file_compiled"])


def detect(diff_text: str, catalog: dict) -> dict:
    """Scan a parsed diff for gaming patterns and build the structured report."""
    flagged: list[dict] = []
    test_files: list[str] = []
    source_files: list[str] = []
    seen: set[tuple] = set()
    for fc in parse_diff(diff_text):
        bucket = test_files if is_test_file(fc["path"], catalog) else source_files
        bucket.append(fc["path"])
        for pat in catalog["patterns"]:
            for lineno, text in fc[pat["applies_to"]]:
                key = (fc["path"], lineno, pat["category"])
                if key in seen or not pat["compiled"].search(text):
                    continue
                seen.add(key)
                flagged.append({
                    "file": fc["path"],
                    "line": lineno,
                    "category": pat["category"],
                    "severity": pat["severity"],
                    "pattern": pat["description"],
                    "snippet": text.strip()[:200],
                })
    summary = {s: sum(f["severity"] == s for f in flagged) for s in SEVERITIES}
    return {
        "flagged": flagged,
        "test_files_touched": test_files,
        "source_files_touched": source_files,
        "summary": summary,
        "verdict": "review" if flagged else "clean",
    }


def main(argv: list[str]) -> int:
    """CLI: read a diff from a file argument or stdin, print the JSON report."""
    if len(argv) > 2:
        print("usage: detect_cheats.py [diff_file]", file=sys.stderr)
        return 2
    try:
        if len(argv) == 2:
            diff_text = Path(argv[1]).read_text(errors="replace")
        else:
            diff_text = sys.stdin.buffer.read().decode(errors="replace")
    except OSError as exc:
        print(f"error: cannot read diff: {exc}", file=sys.stderr)
        return 1
    try:
        catalog = load_catalog()
    except (OSError, json.JSONDecodeError, re.error) as exc:
        print(f"error: cannot load pattern catalog: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(detect(diff_text, catalog), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
