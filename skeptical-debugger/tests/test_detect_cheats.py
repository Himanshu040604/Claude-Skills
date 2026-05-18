"""Unit tests for detect_cheats.py — runs the detector CLI over diff fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "detect_cheats.py"
FIXTURES = Path(__file__).parent / "fixtures"


def run(diff_path: Path) -> tuple[int, dict | None]:
    """Run the detector CLI on a diff file; return (exit_code, parsed_json)."""
    cmd = [sys.executable, str(SCRIPT), str(diff_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(proc.stdout) if proc.stdout.strip() else None
    return proc.returncode, data


def test_clean_fix_verdict_is_clean() -> None:
    code, data = run(FIXTURES / "clean_fix.diff")
    assert code == 0
    assert data is not None
    assert data["verdict"] == "clean"
    assert data["flagged"] == []


@pytest.mark.parametrize("category", [
    "test-skip", "assertion-removed", "error-swallow",
])
def test_cheating_fix_flags_category(category: str) -> None:
    code, data = run(FIXTURES / "cheating_fix.diff")
    assert code == 0
    assert data is not None
    assert data["verdict"] == "review"
    assert category in {f["category"] for f in data["flagged"]}


def test_cheating_fix_touches_test_files() -> None:
    _, data = run(FIXTURES / "cheating_fix.diff")
    assert data is not None
    assert data["test_files_touched"]


def test_output_has_expected_keys() -> None:
    _, data = run(FIXTURES / "clean_fix.diff")
    assert data is not None
    assert set(data) >= {
        "flagged", "test_files_touched", "source_files_touched",
        "summary", "verdict",
    }


def test_malformed_diff_does_not_crash(tmp_path: Path) -> None:
    bad = tmp_path / "bad.diff"
    bad.write_text("this is not a diff\nrandom text\n")
    code, data = run(bad)
    assert code == 0
    assert data is not None
    assert data["verdict"] == "clean"


def test_missing_diff_file_exits_nonzero() -> None:
    code, _ = run(FIXTURES / "does_not_exist.diff")
    assert code == 1


def test_non_utf8_diff_does_not_crash(tmp_path: Path) -> None:
    """B1: a diff with raw binary bytes exits 0 with valid JSON, no traceback."""
    bad = tmp_path / "binary.diff"
    bad.write_bytes(b"--- a/x\n+++ b/x\n@@ -1 +1 @@\n+\xff\xfe\x00\x80 bytes\n")
    code, data = run(bad)
    assert code == 0
    assert data is not None and data["verdict"] in {"clean", "review"}


def test_deleted_test_file_uses_old_path(tmp_path: Path) -> None:
    """B2: a /dev/null whole-file deletion is attributed to its a/... path."""
    diff = tmp_path / "del.diff"
    diff.write_text(
        "--- a/tests/test_x.py\n+++ /dev/null\n"
        "@@ -1,2 +0,0 @@\n-def test_x():\n-    assert True\n"
    )
    code, data = run(diff)
    assert code == 0 and data is not None
    assert "tests/test_x.py" in data["test_files_touched"]
    assert "/dev/null" not in data["source_files_touched"]


def test_conftest_recognized_as_test_file(tmp_path: Path) -> None:
    """B3: a root-level conftest.py is classified as a test file."""
    diff = tmp_path / "conf.diff"
    diff.write_text("--- a/conftest.py\n+++ b/conftest.py\n@@ -0,0 +1 @@\n+import pytest\n")
    code, data = run(diff)
    assert code == 0 and data is not None
    assert "conftest.py" in data["test_files_touched"]
