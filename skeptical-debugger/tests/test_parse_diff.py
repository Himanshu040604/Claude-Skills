"""Direct unit tests for parse_diff.py — exercises the diff parser itself."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parse_diff import parse_diff  # noqa: E402


def test_basic_single_hunk() -> None:
    """A simple one-hunk diff yields correct added/removed lines and numbers."""
    diff = ("--- a/m.py\n+++ b/m.py\n@@ -1,3 +1,3 @@\n"
            " keep\n-old line\n+new line\n unchanged\n")
    [rec] = parse_diff(diff)
    assert rec["path"] == "m.py"
    assert rec["removed"] == [(2, "old line")]
    assert rec["added"] == [(2, "new line")]


def test_removed_line_starting_with_dashdash_is_not_header() -> None:
    """Regression: a removed `-- comment` line stays in removed, not a header."""
    diff = ("--- a/q.sql\n+++ b/q.sql\n@@ -1,3 +1,2 @@\n"
            " SELECT 1;\n--- a comment\n SELECT 2;\n")
    [rec] = parse_diff(diff)
    assert rec["path"] == "q.sql"
    assert rec["removed"] == [(2, "-- a comment")]
    assert rec["added"] == []


def test_added_line_starting_with_plusplus_is_not_header() -> None:
    """An added line whose content starts with `++ ` stays in added."""
    diff = ("--- a/c.cpp\n+++ b/c.cpp\n@@ -1,1 +1,2 @@\n"
            " int x;\n+++ inline marker\n")
    [rec] = parse_diff(diff)
    assert rec["path"] == "c.cpp"
    assert rec["added"] == [(2, "++ inline marker")]
    assert rec["removed"] == []


def test_dev_null_deletion_uses_old_path() -> None:
    """A whole-file deletion to /dev/null keeps the real a/... path."""
    diff = ("--- a/tests/test_x.py\n+++ /dev/null\n"
            "@@ -1,2 +0,0 @@\n-def test_x():\n-    assert True\n")
    [rec] = parse_diff(diff)
    assert rec["path"] == "tests/test_x.py"
    assert rec["removed"] == [(1, "def test_x():"), (2, "    assert True")]


def test_multi_file_diff_yields_multiple_records() -> None:
    """A diff spanning two files yields two records with correct paths."""
    diff = ("--- a/one.py\n+++ b/one.py\n@@ -1 +1 @@\n-a\n+b\n"
            "--- a/two.py\n+++ b/two.py\n@@ -1 +1 @@\n-c\n+d\n")
    recs = parse_diff(diff)
    assert [r["path"] for r in recs] == ["one.py", "two.py"]
    assert recs[0]["added"] == [(1, "b")]
    assert recs[1]["removed"] == [(1, "c")]


def test_no_count_hunk_header_defaults_to_one() -> None:
    """A `@@ -5 +5 @@` header with no counts is parsed (count defaults to 1)."""
    diff = "--- a/n.py\n+++ b/n.py\n@@ -5 +5 @@\n-five\n+FIVE\n"
    [rec] = parse_diff(diff)
    assert rec["removed"] == [(5, "five")]
    assert rec["added"] == [(5, "FIVE")]


def test_no_newline_marker_keeps_line_numbers() -> None:
    """A `\\ No newline` marker interleaved with content is ignored cleanly."""
    diff = ("--- a/f.txt\n+++ b/f.txt\n@@ -1,2 +1,2 @@\n"
            " first\n-second\n\\ No newline at end of file\n"
            "+SECOND\n\\ No newline at end of file\n")
    [rec] = parse_diff(diff)
    assert rec["removed"] == [(2, "second")]
    assert rec["added"] == [(2, "SECOND")]
