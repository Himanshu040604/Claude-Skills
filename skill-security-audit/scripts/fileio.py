"""File-I/O and text-preparation helpers for the danger-pattern scanner.

Static analysis only: reads files as text, never executes their contents.
"""
from __future__ import annotations

from pathlib import Path

_UTF16_BOMS = (b"\xff\xfe", b"\xfe\xff")


def _decode_utf16_no_bom(data: bytes) -> str | None:
    """Decode BOM-less UTF-16, identified by its alternating-NUL pattern.

    ASCII-range UTF-16 text places a NUL in every other byte (odd indices
    for little-endian, even for big-endian); genuine binary scatters NULs
    irregularly. Returns the decoded text, or None if the pattern is absent.
    """
    head = data[:1024]
    head = head[: len(head) - len(head) % 2]
    if not head:
        return None
    even = sum(head[i] == 0 for i in range(0, len(head), 2))
    odd = sum(head[i] == 0 for i in range(1, len(head), 2))
    threshold = len(head) // 8
    if odd > threshold and even == 0:
        encoding = "utf-16-le"
    elif even > threshold and odd == 0:
        encoding = "utf-16-be"
    else:
        return None
    try:
        return data.decode(encoding)
    except (UnicodeDecodeError, ValueError):
        return None


def read_as_text(path: Path) -> str | None:
    """Read a file as text, decoding UTF-16 with or without a BOM.

    UTF-16 text legitimately contains NUL bytes, so it is decoded (by BOM
    when present, else by its alternating-NUL pattern) rather than skipped:
    a skill file cannot evade the scanner by being saved as UTF-16. Returns
    None only when the file is neither valid UTF-8 nor recognizable UTF-16.

    Args:
        path: Path to the file to read.

    Returns:
        The decoded text, or None if the file is binary or unreadable.
    """
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:2] in _UTF16_BOMS:
        try:
            return data.decode("utf-16")
        except (UnicodeDecodeError, ValueError):
            return None
    if b"\x00" not in data[:1024]:
        return data.decode("utf-8", errors="replace")
    return _decode_utf16_no_bom(data)


def logical_lines(text: str) -> list[tuple[int, str]]:
    """Join shell line-continuations into single logical lines.

    A physical line whose text ends with a backslash continues onto the
    next; the joined logical line is reported against its first physical
    line number.

    Args:
        text: Full file text to split into logical lines.

    Returns:
        A list of (first_physical_lineno, joined_text) tuples.
    """
    result: list[tuple[int, str]] = []
    pending: list[str] = []
    start_lineno = 1
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not pending:
            start_lineno = lineno
        if line.endswith("\\"):
            pending.append(line[:-1])
            continue
        pending.append(line)
        result.append((start_lineno, "".join(pending)))
        pending = []
    if pending:
        result.append((start_lineno, "".join(pending)))
    return result
