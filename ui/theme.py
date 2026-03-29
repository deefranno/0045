"""
Global Qt stylesheet for the application.
Applied once to QApplication so every widget inherits it automatically.
Targets are addressed by objectName (#Id) or widget class (QLabel, etc.)
to avoid accidental overrides.
"""

APP_STYLESHEET = """
/* ── Base ─────────────────────────────────────────────────────────────── */
QMainWindow,
QWidget#CentralWidget,
QWidget#ViewContainer {
    background-color: #F4F6F8;
}

QWidget {
    font-family: "Segoe UI", "DejaVu Sans", "Liberation Sans", sans-serif;
    font-size: 13px;
    color: #1C2B3A;
}

/* ── Header bar ───────────────────────────────────────────────────────── */
QFrame#AppHeader {
    background-color: #FFFFFF;
    border-bottom: 1px solid #DDE1E7;
}

QLabel#AppTitle {
    font-size: 17px;
    font-weight: 600;
    color: #1C2B3A;
}

QLabel#AppVersion {
    font-size: 12px;
    color: #9AAABB;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
QWidget#Sidebar {
    background-color: #1E2E3D;
    border-right: 1px solid #162230;
}

QLabel#NavGroupLabel {
    font-size: 10px;
    font-weight: 700;
    color: #4A6880;
    letter-spacing: 1.2px;
    background-color: transparent;
}

QPushButton#NavButton {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    color: #8AAAC4;
    font-size: 13px;
    text-align: left;
    padding: 0 14px;
    margin: 0 8px;
}

QPushButton#NavButton:hover {
    background-color: #26404F;
    color: #D4E6F4;
}

QPushButton#NavButton:checked {
    background-color: #2B5278;
    color: #FFFFFF;
    font-weight: 600;
}

/* ── Status bar ───────────────────────────────────────────────────────── */
QStatusBar {
    background-color: #FFFFFF;
    border-top: 1px solid #DDE1E7;
    color: #607080;
    font-size: 12px;
    padding: 0 8px;
}

QStatusBar::item {
    border: none;
}

/* ── View content area ────────────────────────────────────────────────── */
QLabel#ViewTitle {
    font-size: 20px;
    font-weight: 600;
    color: #1C2B3A;
}

QLabel#ViewSubtitle {
    font-size: 13px;
    color: #5A6E80;
}

/* Placeholder card shown inside each unimplemented view */
QFrame#PlaceholderCard {
    background-color: #FFFFFF;
    border: 1px solid #DDE1E7;
    border-radius: 8px;
}

QLabel#PlaceholderIcon {
    font-size: 32px;
    color: #B0C4D8;
}

QLabel#PlaceholderText {
    font-size: 13px;
    color: #8A9BB0;
}

/* ── General-purpose widgets (future phases) ──────────────────────────── */
QPushButton {
    background-color: #2B5278;
    color: #FFFFFF;
    border: none;
    border-radius: 5px;
    padding: 6px 16px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #336699;
}

QPushButton:pressed {
    background-color: #1E3E5C;
}

QPushButton:disabled {
    background-color: #C8D4E0;
    color: #8A9BB0;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #C8D4E0;
    border-radius: 4px;
    padding: 5px 8px;
    color: #1C2B3A;
    selection-background-color: #2B5278;
    selection-color: #FFFFFF;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #2B5278;
}

QScrollBar:vertical {
    background-color: #F4F6F8;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #C0CCD8;
    border-radius: 4px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9AAABB;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #F4F6F8;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #C0CCD8;
    border-radius: 4px;
    min-width: 24px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #9AAABB;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
}
"""
