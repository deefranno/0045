"""
app.py – application entry point.
Run with:  python3 app.py
"""

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from core.config import APP_NAME, APP_VERSION
from ui.main_window import MainWindow
from ui.theme import APP_STYLESHEET


def main() -> None:
    # High-DPI support (Debian / X11 / Wayland)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
