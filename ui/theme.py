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

/* ── QTabWidget ───────────────────────────────────────────────────────────── */
QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #DDE1E7;
    border-top: none;
    border-radius: 0 0 6px 6px;
}

QTabBar::tab {
    background-color: #EEF2F6;
    border: 1px solid #DDE1E7;
    border-bottom: none;
    padding: 7px 20px;
    font-size: 13px;
    color: #5A6E80;
    margin-right: 2px;
    border-radius: 5px 5px 0 0;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #1C2B3A;
    font-weight: 600;
    border-bottom: 1px solid #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background-color: #E2EAF2;
    color: #1C2B3A;
}

/* ── QTableWidget ─────────────────────────────────────────────────────────── */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #DDE1E7;
    border-radius: 6px;
    gridline-color: #EEF2F6;
    outline: none;
}

QTableWidget::item {
    padding: 5px 10px;
    border: none;
    color: #1C2B3A;
}

QTableWidget::item:selected {
    background-color: #EEF4FB;
    color: #1C2B3A;
}

QHeaderView::section {
    background-color: #F4F6F8;
    border: none;
    border-bottom: 1px solid #DDE1E7;
    border-right: 1px solid #EEF2F6;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 600;
    color: #5A6E80;
    letter-spacing: 0.3px;
}

QHeaderView::section:last {
    border-right: none;
}

/* ── QComboBox ────────────────────────────────────────────────────────────── */
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #C8D4E0;
    border-radius: 4px;
    padding: 5px 10px;
    color: #1C2B3A;
    min-width: 160px;
}

QComboBox:focus {
    border-color: #2B5278;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #C8D4E0;
    border-radius: 4px;
    selection-background-color: #EEF4FB;
    selection-color: #1C2B3A;
    outline: none;
}

/* ── QRadioButton ─────────────────────────────────────────────────────────── */
QRadioButton {
    color: #1C2B3A;
    font-size: 13px;
    spacing: 7px;
}

QRadioButton::indicator {
    width: 15px;
    height: 15px;
    border: 2px solid #9AAABB;
    border-radius: 8px;
    background-color: #FFFFFF;
}

QRadioButton::indicator:checked {
    border-color: #2B5278;
    background-color: #2B5278;
}

QRadioButton::indicator:hover {
    border-color: #2B5278;
}

/* ── Import view specific ─────────────────────────────────────────────────── */
QLabel#SectionLabel {
    font-size: 10px;
    font-weight: 700;
    color: #8A9BB0;
    letter-spacing: 1.2px;
}

QFrame#PreviewSection {
    background-color: transparent;
}

QFrame#SummaryCard {
    background-color: #FFFFFF;
    border: 1px solid #DDE1E7;
    border-left: 4px solid #2E7D4F;
    border-radius: 6px;
}

QLabel#SummaryTitle {
    font-size: 14px;
    font-weight: 600;
    color: #2E7D4F;
}

QLabel#SummaryLine {
    font-size: 13px;
    color: #3A4A5A;
}

QLabel#ErrorLabel {
    font-size: 13px;
    color: #B22222;
    padding: 6px 0;
}

QLabel#FileLabel {
    font-size: 12px;
    color: #5A6E80;
    font-style: italic;
}

QPushButton#ImportButton {
    background-color: #2E7D4F;
    color: #FFFFFF;
    border: none;
    border-radius: 5px;
    padding: 8px 24px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#ImportButton:hover {
    background-color: #379660;
}

QPushButton#ImportButton:disabled {
    background-color: #C8D4E0;
    color: #8A9BB0;
}

QPushButton#SecondaryButton {
    background-color: #FFFFFF;
    color: #2B5278;
    border: 1px solid #C8D4E0;
    border-radius: 5px;
    font-size: 13px;
    padding: 5px 14px;
}

QPushButton#SecondaryButton:hover {
    background-color: #EEF4FB;
    border-color: #2B5278;
}

/* ── Search Queue / action toolbar ───────────────────────────────────────── */
QFrame#ActionBar {
    background-color: #FFFFFF;
    border: 1px solid #DDE1E7;
    border-radius: 6px;
}

QLabel#StatsLabel {
    font-size: 12px;
    color: #607080;
}

QLabel#TableHint {
    font-size: 12px;
    color: #9AAABB;
    font-style: italic;
}
"""
