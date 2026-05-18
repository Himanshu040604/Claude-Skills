#!/usr/bin/env python3
"""Mechanical danger-pattern scanner for Claude skill packages.

Static analysis only: never imports, evaluates, or executes scanned files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from fileio import logical_lines, read_as_text

SEVERITIES = ("critical", "high", "medium", "low", "info")


def load_patterns() -> list[dict]:
    """Load and pre-compile the danger-pattern catalog from patterns.json."""
    catalog = Path(__file__).parent / "patterns.json"
    patterns = json.loads(catalog.read_text())["patterns"]
    for pat in patterns:
        pat["compiled"] = re.compile(pat["regex"])
    return patterns


def scan_file(rel: str, text: str, patterns: list[dict]) -> list[dict]:
    """Apply every catalog pattern to one file's text, logical line by line.

    Shell line-continuations are joined first so a pattern split across
    physical lines is still matched; findings report the first physical
    line number of the joined logical line.
    """
    findings: list[dict] = []
    for lineno, line in logical_lines(text):
        for pat in patterns:
            if pat["compiled"].search(line):
                findings.append({
                    "file": rel,
                    "line": lineno,
                    "category": pat["category"],
                    "severity": pat["severity"],
                    "pattern": pat["description"],
                    "snippet": line.strip()[:200],
                })
    return findings


def scan(skill_path: Path) -> dict:
    """Scan every text file under skill_path and build the findings report."""
    patterns = load_patterns()
    findings: list[dict] = []
    scanned = 0
    skipped: list[str] = []
    for path in sorted(p for p in skill_path.rglob("*") if p.is_file()):
        rel = str(path.relative_to(skill_path))
        text = read_as_text(path)
        if text is None:
            skipped.append(f"{rel} (binary)")
            continue
        findings.extend(scan_file(rel, text, patterns))
        scanned += 1
    summary = {s: sum(f["severity"] == s for f in findings) for s in SEVERITIES}
    return {
        "skill_path": str(skill_path),
        "files_scanned": scanned,
        "files_skipped": skipped,
        "findings": findings,
        "summary": summary,
    }


def main(argv: list[str]) -> int:
    """CLI: scan the given skill folder, print JSON, return an exit code."""
    if len(argv) != 2:
        print("usage: scan_patterns.py <skill_path>", file=sys.stderr)
        return 2
    skill_path = Path(argv[1])
    if not skill_path.is_dir():
        print(f"error: not a directory: {skill_path}", file=sys.stderr)
        return 1
    try:
        report = scan(skill_path)
    except (OSError, json.JSONDecodeError, re.error, KeyError, TypeError) as exc:
        print(f"error: cannot load pattern catalog: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
