#!/usr/bin/env python3
"""Parse a unified diff into structured per-file added/removed lines.

Best-effort and exception-free: malformed input yields a partial result.
"""
from __future__ import annotations

import re

_HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _header_path(line: str) -> str:
    """Extract a clean file path from a `--- ` or `+++ ` header line."""
    path = line[4:].split("\t", 1)[0].strip()
    return path[2:] if path[:2] in ("a/", "b/") else path


def parse_diff(diff_text: str) -> list[dict]:
    """Parse unified-diff text into per-file change records.

    Each record is {"path": str, "added": [(lineno, text)],
    "removed": [(lineno, text)]}. Added line numbers are new-file numbers;
    removed line numbers are old-file numbers. Hunk line counts from each
    @@ header bound the hunk, so diff *content* lines that begin with
    `--- `/`+++ ` are not mistaken for file headers.
    """
    files: list[dict] = []
    current: dict | None = None
    old_path = ""
    old_no = new_no = old_left = new_left = 0
    for line in diff_text.splitlines():
        if old_left > 0 or new_left > 0:
            if line.startswith("\\ "):
                continue
            if line.startswith("+"):
                if current is not None:
                    current["added"].append((new_no, line[1:]))
                new_no, new_left = new_no + 1, new_left - 1
            elif line.startswith("-"):
                if current is not None:
                    current["removed"].append((old_no, line[1:]))
                old_no, old_left = old_no + 1, old_left - 1
            else:
                old_no, new_no = old_no + 1, new_no + 1
                old_left, new_left = old_left - 1, new_left - 1
            continue
        if hunk := _HUNK.match(line):
            old_no, old_left = int(hunk.group(1)), int(hunk.group(2) or 1)
            new_no, new_left = int(hunk.group(3)), int(hunk.group(4) or 1)
        elif line.startswith("--- "):
            old_path = _header_path(line)
        elif line.startswith("+++ "):
            path = _header_path(line)
            current = {"path": old_path if path == "/dev/null" else path,
                       "added": [], "removed": []}
            files.append(current)
    return files
