"""
app.py – application entry point.
Run with:  python3 app.py
"""

import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from core.config import APP_NAME, APP_VERSION, DB_PATH
from core.database import DatabaseManager
from core.repository import ProductRepository
from ui.main_window import MainWindow
from ui.theme import APP_STYLESHEET

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting %s v%s", APP_NAME, APP_VERSION)

    # ── Database ──────────────────────────────────────────────────────────
    db = DatabaseManager(DB_PATH)
    db.initialize()         # creates tables on first run; no-op afterwards
    repo = ProductRepository(db)

    # ── Qt application ────────────────────────────────────────────────────
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow(repo)
    window.show()

    logger.info("UI ready")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
