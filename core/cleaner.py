"""
Product name cleaning engine.

Converts raw stock-list names (ALL CAPS, pack sizes, abbreviations, stock codes)
into clean, search-friendly strings using regex-based heuristics.

Pipeline (applied in order):
  1. Replace separator characters  (_ → space)
  2. Strip stock-code prefixes      (SKU001 Widget → Widget)
  3. Remove pack-multiplier sizes   (12X330ML, 24*250ML)
  4. Remove standalone sizes        (500ML, 1.5KG, 200G)
  5. Remove pack-count suffixes     (6PK, 24CT, 12PACK)
  6. Expand abbreviations           (BTL→Bottle, ORIG→Original)
  7. Normalize whitespace
  8. Apply Title Case if original was ALL CAPS

The ABBREVIATION_MAP is the single place to add or change expansions.
No other code changes are needed to extend it.
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ── Abbreviation expansion map ────────────────────────────────────────────────
# Keys  : matched as whole words, case-insensitive.
# Values: replacement string.  Empty string removes the token entirely.
# Add new entries here freely — the regex is rebuilt from this dict at import time.

ABBREVIATION_MAP: dict[str, str] = {
    # ── Packaging containers ─────────────────────────────────────────────────
    "BTL":     "Bottle",
    "BTLS":    "Bottles",
    "PKT":     "Packet",
    "PKTS":    "Packets",
    "PKG":     "Package",
    "TIN":     "Tin",
    "TINS":    "Tins",
    "CAN":     "Can",
    "CANS":    "Cans",
    "JAR":     "Jar",
    "JARS":    "Jars",
    "BAG":     "Bag",
    "BAGS":    "Bags",
    "BOX":     "Box",
    "BXS":     "Boxes",
    "SACHET":  "Sachet",
    "SACHETS": "Sachets",
    "TUBE":    "Tube",
    "TUBES":   "Tubes",
    "DRUM":    "Drum",
    "DRUMS":   "Drums",
    "POUCH":   "Pouch",
    "POUCHES": "Pouches",
    "TRAY":    "Tray",
    "TRAYS":   "Trays",
    "WRAP":    "Wrap",
    "WRAPS":   "Wraps",
    # ── Descriptors ──────────────────────────────────────────────────────────
    "ORIG":    "Original",
    "ORGINAL": "Original",   # common misspelling in stock data
    "ORG":     "Organic",
    "REG":     "Regular",
    "STD":     "Standard",
    "PREM":    "Premium",
    "SPEC":    "Special",
    "LTD":     "Limited",
    "ASSORT":  "Assorted",
    "ASST":    "Assorted",
    "VAR":     "Various",
    "VARS":    "Various",
    "UNFLAVD": "Unflavoured",
    "UNSWT":   "Unsweetened",
    "WHSLE":   "Wholesale",
    "WNTR":    "Winter",
    "SUMR":    "Summer",
    # ── Size/format descriptors (words, not measurements) ────────────────────
    "LGE":     "Large",
    "LRGE":    "Large",
    "MED":     "Medium",
    "MINI":    "Mini",
    "MINIS":   "Mini",
    "SNGL":    "Single",
    "DBL":     "Double",
    "TWIN":    "Twin",
    "MULTI":   "Multi",
    "BULK":    "Bulk",
    # ── Tokens to silently remove (empty replacement) ────────────────────────
    "TBC":     "",
    "TBA":     "",
    "DISC":    "",   # "discontinued" code sometimes appended
    "DISCONT": "",
}


# ── Compiled regex patterns ───────────────────────────────────────────────────

# Units of measurement — listed longest-first so alternation matches greedily.
_UNIT_LIST: list[str] = [
    "FLOZ", "PINTS", "PINT", "GALS", "GAL",
    "LTRS", "LTR", "KGS", "KG", "GRM", "GRS", "GR", "GM",
    "LBS", "LB", "ML", "CL", "OZ", "G", "L",
]
_UNITS = "(?:" + "|".join(_UNIT_LIST) + ")"

# 12X330ML  24*250ML  6 x 440ml  10×1.5KG
_RE_PACK_MULTIPLIER: re.Pattern = re.compile(
    r"\b\d+\s*[Xx*×]\s*\d+(?:\.\d+)?\s*" + _UNITS + r"\b",
    re.IGNORECASE,
)

# 500ML  1.5L  200G  6OZ  (standalone — must run after pack-multiplier)
_RE_STANDALONE_SIZE: re.Pattern = re.compile(
    r"\b\d+(?:\.\d+)?\s*" + _UNITS + r"\b",
    re.IGNORECASE,
)

# 6PK  24CT  12PACK  3PC  18EA
_RE_PACK_COUNT: re.Pattern = re.compile(
    r"\b\d+\s*(?:PK|PKS|PCS|PC|CT|CTS|EA|EACH|PACK|PACKS|PIECE|PIECES|UNIT|UNITS|COUNT)\b",
    re.IGNORECASE,
)

# Stock-code prefix at the start: SKU001, AB-123, REF_99, or a bare 4-digit number
_RE_STOCK_CODE_PREFIX: re.Pattern = re.compile(
    r"^(?:[A-Z]{1,8}[-_]?\d{2,}|\d{4,})\s+(?=\S)",
    re.IGNORECASE,
)

# Built once from ABBREVIATION_MAP — call _build_abbrev_pattern() below
def _build_abbrev_pattern() -> re.Pattern:
    # Longest keys first so multi-word abbreviations aren't partially matched
    keys = sorted(ABBREVIATION_MAP.keys(), key=len, reverse=True)
    escaped = [re.escape(k) for k in keys]
    return re.compile(r"\b(?:" + "|".join(escaped) + r")\b", re.IGNORECASE)

_RE_ABBREVIATIONS: re.Pattern = _build_abbrev_pattern()


# ── Public API ────────────────────────────────────────────────────────────────


@dataclass
class CleanResult:
    original: str
    cleaned: str

    @property
    def changed(self) -> bool:
        return self.original != self.cleaned


def clean(name: str) -> str:
    """Run the full cleaning pipeline on one product name string."""
    if not name or not name.strip():
        return name

    original = name.strip()
    text = original

    text = _remove_stock_code_prefix(text)  # must run before separators are replaced
    text = _replace_separators(text)
    text = _remove_pack_multiplier_sizes(text)
    text = _remove_standalone_sizes(text)
    text = _remove_pack_counts(text)
    text = _expand_abbreviations(text)
    text = _normalize_spacing(text)
    text = _apply_title_case(original, text)

    logger.debug("clean: %r → %r", original, text)
    return text


def clean_batch(names: list[str]) -> list[CleanResult]:
    """Clean a list of names; returns one CleanResult per input."""
    return [CleanResult(original=n, cleaned=clean(n)) for n in names]


# ── Pipeline steps (private) ──────────────────────────────────────────────────


def _replace_separators(text: str) -> str:
    """Replace underscores (common in database exports) with spaces."""
    return text.replace("_", " ")


def _remove_stock_code_prefix(text: str) -> str:
    """Strip a leading stock/SKU code if the name would still have content."""
    stripped = _RE_STOCK_CODE_PREFIX.sub("", text).strip()
    # Guard: never return an empty string just because a prefix was removed
    return stripped if stripped else text


def _remove_pack_multiplier_sizes(text: str) -> str:
    """Remove pack×unit patterns: 12X330ML, 24*250ML, 6 x 440ml."""
    return _RE_PACK_MULTIPLIER.sub(" ", text)


def _remove_standalone_sizes(text: str) -> str:
    """Remove standalone measurement tokens: 500ML, 1.5KG, 200G."""
    return _RE_STANDALONE_SIZE.sub(" ", text)


def _remove_pack_counts(text: str) -> str:
    """Remove pack-count tokens: 6PK, 24CT, 12PACK, 3PC."""
    return _RE_PACK_COUNT.sub(" ", text)


def _expand_abbreviations(text: str) -> str:
    """Replace known abbreviation tokens with their full-word equivalents."""
    def _replace(match: re.Match) -> str:
        key = match.group(0).upper()
        return ABBREVIATION_MAP.get(key, match.group(0))

    return _RE_ABBREVIATIONS.sub(_replace, text)


def _normalize_spacing(text: str) -> str:
    """Collapse multiple spaces to one and strip leading/trailing whitespace."""
    return " ".join(text.split())


def _apply_title_case(original: str, processed: str) -> str:
    """Apply Title Case when the original is predominantly uppercase.

    Threshold: 60% of alphabetic characters are uppercase.
    This handles stock lists where names are ALLCAPS but measurements
    are mixed (e.g. '12X330ml', '6 x 440ml') without misidentifying
    properly title-cased brand names like 'Fairy Liquid Original'.
    """
    alpha_chars = [c for c in original if c.isalpha()]
    if not alpha_chars:
        return processed
    upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
    if upper_ratio >= 0.6:
        return processed.title()
    return processed
