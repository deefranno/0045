"""
Parsing and preview logic for product name import.

All file I/O and normalization logic lives here — no UI dependencies.
The UI layer calls these functions and receives plain data structures back.

Encoding strategy for files:
  1. utf-8-sig  — handles Excel-exported CSVs with a BOM
  2. utf-8      — standard
  3. latin-1    — safe fallback for Windows CP1252 exports; never raises UnicodeDecodeError
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_ENCODINGS = ["utf-8-sig", "utf-8", "latin-1"]


# ── Result types ──────────────────────────────────────────────────────────────


@dataclass
class ParseResult:
    """Raw output from any parse function, before duplicate-checking."""
    names: list[str]   # cleaned, non-blank names; may contain within-batch dupes
    total_rows: int    # lines/rows read including blanks
    blank_removed: int # blank rows stripped
    source: str        # human-readable description for the UI


@dataclass
class PreviewRow:
    """One row in the import preview table."""
    name: str
    is_db_duplicate: bool    # already exists in the database
    is_batch_duplicate: bool # appeared earlier in this same import batch

    @property
    def is_any_duplicate(self) -> bool:
        return self.is_db_duplicate or self.is_batch_duplicate


@dataclass
class ImportSummary:
    total_rows: int
    valid_names: int       # non-blank after cleaning
    duplicates_skipped: int
    imported: int


# ── Public parse functions ────────────────────────────────────────────────────


def parse_txt(path: Path) -> ParseResult:
    """Read a plain-text file — one product name per line."""
    text = _read_text(path)
    lines = text.splitlines()
    names, blank_count = _normalize_lines(lines)
    logger.debug("TXT '%s': %d lines, %d blank removed", path.name, len(lines), blank_count)
    return ParseResult(
        names=names,
        total_rows=len(lines),
        blank_removed=blank_count,
        source=path.name,
    )


def get_csv_columns(path: Path) -> list[str]:
    """Return the header column names from a CSV file (first row only)."""
    text = _read_text(path)
    reader = csv.reader(text.splitlines())
    try:
        headers = next(reader)
    except StopIteration:
        return []
    return [h.strip() for h in headers if h.strip()]


def parse_csv(path: Path, column: str) -> ParseResult:
    """Read a CSV and extract product names from the specified column."""
    text = _read_text(path)
    lines = text.splitlines()
    if not lines:
        return ParseResult(names=[], total_rows=0, blank_removed=0, source=path.name)

    reader = csv.DictReader(lines)
    available = list(reader.fieldnames or [])

    if column not in available:
        raise ValueError(
            f"Column '{column}' not found in {path.name}.\n"
            f"Available columns: {', '.join(available)}"
        )

    raw_names = [str(row.get(column, "") or "") for row in reader]
    data_rows = len(raw_names)
    names, blank_count = _normalize_lines(raw_names)
    logger.debug(
        "CSV '%s' col='%s': %d rows, %d blank removed",
        path.name, column, data_rows, blank_count,
    )
    return ParseResult(
        names=names,
        total_rows=data_rows,
        blank_removed=blank_count,
        source=f"{path.name}  (column: {column})",
    )


def parse_paste(text: str) -> ParseResult:
    """Parse newline-separated product names from pasted text."""
    lines = text.splitlines()
    names, blank_count = _normalize_lines(lines)
    logger.debug("Paste: %d lines, %d blank removed", len(lines), blank_count)
    return ParseResult(
        names=names,
        total_rows=len(lines),
        blank_removed=blank_count,
        source="pasted text",
    )


# ── Preview builder ───────────────────────────────────────────────────────────


def build_preview_rows(
    names: list[str],
    existing_lower: set[str],
) -> list[PreviewRow]:
    """
    Tag each name as a DB duplicate, a within-batch duplicate, or new.

    existing_lower  — lowercase-stripped original_names already in the database
                      (obtained from ProductRepository.get_all_original_names_lower())
    """
    seen_in_batch: set[str] = set()
    rows: list[PreviewRow] = []
    for name in names:
        key = name.lower().strip()
        is_db_dup = key in existing_lower
        is_batch_dup = key in seen_in_batch
        seen_in_batch.add(key)
        rows.append(PreviewRow(
            name=name,
            is_db_duplicate=is_db_dup,
            is_batch_duplicate=is_batch_dup,
        ))
    return rows


# ── Private helpers ───────────────────────────────────────────────────────────


def _read_text(path: Path) -> str:
    """Try multiple encodings in order; raise a user-friendly ValueError on failure."""
    for encoding in _ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(
        f"Could not decode '{path.name}'.\n"
        "Please re-save the file as UTF-8 and try again."
    )


def _normalize_lines(lines: list[str]) -> tuple[list[str], int]:
    """Strip whitespace, remove blank lines. Returns (clean_names, blank_count)."""
    cleaned: list[str] = []
    blank_count = 0
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned.append(stripped)
        else:
            blank_count += 1
    return cleaned, blank_count
