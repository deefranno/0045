"""
Application-wide constants and configuration.
No runtime logic lives here — only static values.
"""

from pathlib import Path

APP_NAME = "Product Image Finder"
APP_VERSION = "0.3.0"

# ── Filesystem paths ──────────────────────────────────────────────────────────
# PROJECT_ROOT is the directory that contains app.py (one level up from core/).
PROJECT_ROOT: Path = Path(__file__).parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
DB_PATH: Path = DATA_DIR / "products.db"

# Main window defaults
APP_MIN_WIDTH = 1100
APP_MIN_HEIGHT = 700
APP_DEFAULT_WIDTH = 1280
APP_DEFAULT_HEIGHT = 800

# Sidebar
SIDEBAR_WIDTH = 220

# Navigation section order and display names
NAV_SECTIONS: list[str] = [
    "Dashboard",
    "Import Products",
    "Search Queue",
    "Review Images",
    "Exports",
    "Settings",
]

# Unicode glyphs used as lightweight nav icons (no icon font dependency)
NAV_GLYPHS: dict[str, str] = {
    "Dashboard":       "▦",
    "Import Products": "⊕",
    "Search Queue":    "⊙",
    "Review Images":   "◫",
    "Exports":         "↗",
    "Settings":        "⚙",
}
