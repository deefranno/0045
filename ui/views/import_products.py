"""
Import Products view.

Workflow:
  1. Pick a TXT / CSV file  OR  paste names into the text area.
  2. Preview loads automatically (TXT/paste) or after column selection (CSV).
  3. Choose duplicate handling: skip or import anyway.
  4. Click Import — summary shown inline.
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.importer import (
    ImportSummary,
    ParseResult,
    PreviewRow,
    build_preview_rows,
    get_csv_columns,
    parse_csv,
    parse_paste,
    parse_txt,
)
from core.repository import ProductRepository

logger = logging.getLogger(__name__)

# Table column indices
_COL_NUM = 0
_COL_NAME = 1
_COL_STATUS = 2

# Row colours in the preview table
_COLOR_NEW_BG = QColor("#F6FBF8")
_COLOR_NEW_FG = QColor("#2E7D4F")
_COLOR_DUP_BG = QColor("#FAFAFA")
_COLOR_DUP_FG = QColor("#9AAABB")


class ImportProductsView(QWidget):
    def __init__(self, repo: ProductRepository, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._repo = repo

        # State
        self._parse_result: ParseResult | None = None
        self._preview_rows: list[PreviewRow] = []
        self._csv_path: Path | None = None

        # Widgets assigned during _build (referenced in slots)
        self._file_label: QLabel
        self._csv_column_row: QWidget
        self._csv_column_combo: QComboBox
        self._paste_area: QPlainTextEdit
        self._preview_section: QFrame
        self._preview_count_label: QLabel
        self._skip_radio: QRadioButton
        self._import_anyway_radio: QRadioButton
        self._table: QTableWidget
        self._import_btn: QPushButton
        self._error_label: QLabel
        self._summary_section: QFrame
        self._summary_label: QLabel

        self._build()

    # ── Construction ──────────────────────────────────────────────────────

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 24)
        root.setSpacing(0)

        # Page header
        title = QLabel("Import Products")
        title.setObjectName("ViewTitle")
        root.addWidget(title)
        root.addSpacing(4)

        subtitle = QLabel(
            "Load a .txt or .csv file, or paste names directly. "
            "Preview before saving — duplicates are flagged automatically."
        )
        subtitle.setObjectName("ViewSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)
        root.addSpacing(20)

        # Source tabs
        source_label = QLabel("SOURCE")
        source_label.setObjectName("SectionLabel")
        root.addWidget(source_label)
        root.addSpacing(6)
        root.addWidget(self._build_source_tabs())
        root.addSpacing(20)

        # Error label (hidden until needed)
        self._error_label = QLabel("")
        self._error_label.setObjectName("ErrorLabel")
        self._error_label.setVisible(False)
        self._error_label.setWordWrap(True)
        root.addWidget(self._error_label)

        # Preview section (hidden until data is loaded)
        self._preview_section = self._build_preview_section()
        self._preview_section.setVisible(False)
        root.addWidget(self._preview_section, stretch=1)
        root.addSpacing(12)

        # Summary card (hidden until after import)
        self._summary_section = self._build_summary_section()
        self._summary_section.setVisible(False)
        root.addWidget(self._summary_section)

    def _build_source_tabs(self) -> QTabWidget:
        tabs = QTabWidget()
        tabs.setMaximumHeight(220)
        tabs.addTab(self._build_file_tab(), "  From File  ")
        tabs.addTab(self._build_paste_tab(), "  Paste Text  ")
        return tabs

    def _build_file_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        # File picker buttons
        btn_row = QWidget()
        btn_layout = QHBoxLayout(btn_row)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(10)

        pick_txt_btn = QPushButton("Pick TXT File")
        pick_txt_btn.setObjectName("SecondaryButton")
        pick_txt_btn.setFixedWidth(130)
        pick_txt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pick_txt_btn.clicked.connect(self._on_pick_txt)

        pick_csv_btn = QPushButton("Pick CSV File")
        pick_csv_btn.setObjectName("SecondaryButton")
        pick_csv_btn.setFixedWidth(130)
        pick_csv_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pick_csv_btn.clicked.connect(self._on_pick_csv)

        btn_layout.addWidget(pick_txt_btn)
        btn_layout.addWidget(pick_csv_btn)
        btn_layout.addStretch()
        layout.addWidget(btn_row)

        # Selected file label
        self._file_label = QLabel("No file selected.")
        self._file_label.setObjectName("FileLabel")
        layout.addWidget(self._file_label)

        # CSV column selector (hidden unless a CSV is loaded)
        self._csv_column_row = QWidget()
        col_row_layout = QHBoxLayout(self._csv_column_row)
        col_row_layout.setContentsMargins(0, 0, 0, 0)
        col_row_layout.setSpacing(10)

        col_label = QLabel("Name column:")
        col_label.setFixedWidth(100)
        self._csv_column_combo = QComboBox()
        self._csv_column_combo.setMinimumWidth(200)
        self._csv_column_combo.currentTextChanged.connect(self._on_csv_column_changed)

        col_row_layout.addWidget(col_label)
        col_row_layout.addWidget(self._csv_column_combo)
        col_row_layout.addStretch()

        self._csv_column_row.setVisible(False)
        layout.addWidget(self._csv_column_row)
        layout.addStretch()

        return widget

    def _build_paste_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        hint = QLabel("One product name per line:")
        hint.setObjectName("FileLabel")
        layout.addWidget(hint)

        self._paste_area = QPlainTextEdit()
        self._paste_area.setPlaceholderText(
            "Widget Pro 500ml\nGadget Blue XL\nAccessory Kit v2\n…"
        )
        layout.addWidget(self._paste_area, stretch=1)

        load_btn = QPushButton("Load Preview")
        load_btn.setObjectName("SecondaryButton")
        load_btn.setFixedWidth(130)
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_btn.clicked.connect(self._on_load_paste_preview)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(load_btn)
        layout.addLayout(btn_row)

        return widget

    def _build_preview_section(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("PreviewSection")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header row: count label + duplicate options
        header_row = QWidget()
        header_layout = QHBoxLayout(header_row)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        preview_section_label = QLabel("PREVIEW")
        preview_section_label.setObjectName("SectionLabel")
        header_layout.addWidget(preview_section_label)
        header_layout.addSpacing(12)

        self._preview_count_label = QLabel("")
        self._preview_count_label.setObjectName("ViewSubtitle")
        header_layout.addWidget(self._preview_count_label)
        header_layout.addStretch()

        # Duplicate handling radio buttons
        dup_label = QLabel("Duplicates:")
        dup_label.setObjectName("FileLabel")
        header_layout.addWidget(dup_label)
        header_layout.addSpacing(8)

        self._skip_radio = QRadioButton("Skip")
        self._import_anyway_radio = QRadioButton("Import anyway")
        self._skip_radio.setChecked(True)

        dup_group = QButtonGroup(self)
        dup_group.addButton(self._skip_radio)
        dup_group.addButton(self._import_anyway_radio)
        self._skip_radio.toggled.connect(self._update_import_button)

        header_layout.addWidget(self._skip_radio)
        header_layout.addSpacing(12)
        header_layout.addWidget(self._import_anyway_radio)

        layout.addWidget(header_row)

        # Preview table
        self._table = QTableWidget(0, 3)
        self._table.setHorizontalHeaderLabels(["#", "Product Name", "Status"])
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_NUM, QHeaderView.ResizeMode.Fixed
        )
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_NAME, QHeaderView.ResizeMode.Stretch
        )
        self._table.horizontalHeader().setSectionResizeMode(
            _COL_STATUS, QHeaderView.ResizeMode.Fixed
        )
        self._table.setColumnWidth(_COL_NUM, 52)
        self._table.setColumnWidth(_COL_STATUS, 110)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(False)
        self._table.setShowGrid(True)
        layout.addWidget(self._table, stretch=1)

        # Footer: import button
        footer_row = QWidget()
        footer_layout = QHBoxLayout(footer_row)
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.setSpacing(0)
        footer_layout.addStretch()

        self._import_btn = QPushButton("Import Products")
        self._import_btn.setObjectName("ImportButton")
        self._import_btn.setFixedWidth(220)
        self._import_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._import_btn.clicked.connect(self._on_import_clicked)
        footer_layout.addWidget(self._import_btn)

        layout.addWidget(footer_row)
        return frame

    def _build_summary_section(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("SummaryCard")
        frame.setFixedHeight(110)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(6)

        self._summary_title = QLabel("Import complete")
        self._summary_title.setObjectName("SummaryTitle")
        layout.addWidget(self._summary_title)

        self._summary_label = QLabel("")
        self._summary_label.setObjectName("SummaryLine")
        self._summary_label.setWordWrap(True)
        layout.addWidget(self._summary_label)

        reset_btn = QPushButton("Import More")
        reset_btn.setObjectName("SecondaryButton")
        reset_btn.setFixedWidth(110)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._reset)
        layout.addWidget(reset_btn)

        return frame

    # ── Slots / event handlers ────────────────────────────────────────────

    def _on_pick_txt(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Open TXT File",
            "",
            "Text files (*.txt);;All files (*)",
        )
        if not path_str:
            return
        path = Path(path_str)
        self._csv_column_row.setVisible(False)
        self._csv_path = None
        try:
            result = parse_txt(path)
        except ValueError as exc:
            self._show_error(str(exc))
            return
        self._file_label.setText(f"Selected: {path.name}  ({result.total_rows} lines)")
        self._load_preview(result)

    def _on_pick_csv(self) -> None:
        path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV File",
            "",
            "CSV files (*.csv);;All files (*)",
        )
        if not path_str:
            return
        path = Path(path_str)
        self._csv_path = path

        try:
            columns = get_csv_columns(path)
        except ValueError as exc:
            self._show_error(str(exc))
            return

        if not columns:
            self._show_error(f"No header columns found in {path.name}.")
            return

        # Populate combo — block signals while rebuilding to avoid spurious triggers
        self._csv_column_combo.blockSignals(True)
        self._csv_column_combo.clear()
        self._csv_column_combo.addItems(columns)
        self._csv_column_combo.blockSignals(False)

        self._file_label.setText(f"Selected: {path.name}")
        self._csv_column_row.setVisible(True)

        # Trigger an initial parse with the first column
        self._on_csv_column_changed(self._csv_column_combo.currentText())

    def _on_csv_column_changed(self, column: str) -> None:
        if not self._csv_path or not column:
            return
        try:
            result = parse_csv(self._csv_path, column)
        except ValueError as exc:
            self._show_error(str(exc))
            return
        self._load_preview(result)

    def _on_load_paste_preview(self) -> None:
        text = self._paste_area.toPlainText().strip()
        if not text:
            self._show_error("Paste area is empty. Enter at least one product name.")
            return
        result = parse_paste(text)
        if not result.names:
            self._show_error("No valid product names found in pasted text.")
            return
        self._load_preview(result)

    def _on_import_clicked(self) -> None:
        names = self._get_names_to_import()
        if not names:
            self._show_error("Nothing to import with the current settings.")
            return

        # Count what we're skipping for the summary
        all_names = [r.name for r in self._preview_rows]
        skipping = len(all_names) - len(names) if self._skip_radio.isChecked() else 0

        try:
            imported = self._repo.create_batch(names)
        except Exception as exc:
            logger.exception("Import failed")
            self._show_error(f"Import failed: {exc}")
            return

        parse = self._parse_result
        summary = ImportSummary(
            total_rows=parse.total_rows if parse else 0,
            valid_names=len(self._preview_rows),
            duplicates_skipped=skipping,
            imported=imported,
        )
        logger.info(
            "Import complete: %d imported, %d skipped, source=%s",
            imported, skipping, parse.source if parse else "?",
        )
        self._show_summary(summary)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _load_preview(self, result: ParseResult) -> None:
        """Build preview rows from a ParseResult and show the preview section."""
        self._hide_error()
        self._summary_section.setVisible(False)
        self._parse_result = result

        existing = self._repo.get_all_original_names_lower()
        self._preview_rows = build_preview_rows(result.names, existing)

        self._populate_table()
        self._update_import_button()

        total = len(self._preview_rows)
        dups = sum(1 for r in self._preview_rows if r.is_any_duplicate)
        new = total - dups
        self._preview_count_label.setText(
            f"{total} product{'s' if total != 1 else ''} · "
            f"{new} new · {dups} duplicate{'s' if dups != 1 else ''}"
        )
        self._preview_section.setVisible(True)

    def _populate_table(self) -> None:
        self._table.setRowCount(0)
        self._table.setRowCount(len(self._preview_rows))

        for i, row in enumerate(self._preview_rows):
            is_dup = row.is_any_duplicate

            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            num_item.setForeground(_COLOR_DUP_FG if is_dup else _COLOR_NEW_FG)

            name_item = QTableWidgetItem(row.name)
            name_item.setForeground(_COLOR_DUP_FG if is_dup else QColor("#1C2B3A"))

            if row.is_batch_duplicate:
                status_text = "Batch dup."
                status_fg = QColor("#C07000")
            elif row.is_db_duplicate:
                status_text = "In DB"
                status_fg = _COLOR_DUP_FG
            else:
                status_text = "New"
                status_fg = _COLOR_NEW_FG

            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(status_fg)

            bg = _COLOR_DUP_BG if is_dup else _COLOR_NEW_BG
            for item in (num_item, name_item, status_item):
                item.setBackground(bg)

            self._table.setItem(i, _COL_NUM, num_item)
            self._table.setItem(i, _COL_NAME, name_item)
            self._table.setItem(i, _COL_STATUS, status_item)

        self._table.resizeRowsToContents()

    def _update_import_button(self) -> None:
        names = self._get_names_to_import()
        count = len(names)
        if count == 0:
            self._import_btn.setText("Nothing to Import")
            self._import_btn.setEnabled(False)
        else:
            self._import_btn.setText(f"Import {count} Product{'s' if count != 1 else ''}")
            self._import_btn.setEnabled(True)

    def _get_names_to_import(self) -> list[str]:
        """Return the list of names that will be inserted, given current options."""
        if self._skip_radio.isChecked():
            # Skip anything flagged as a duplicate (DB or within-batch)
            return [r.name for r in self._preview_rows if not r.is_any_duplicate]
        else:
            # Import anyway: include DB duplicates but still skip within-batch dupes
            # (prevents inserting the same name N times in one batch)
            seen: set[str] = set()
            result: list[str] = []
            for r in self._preview_rows:
                if not r.is_batch_duplicate:
                    key = r.name.lower().strip()
                    if key not in seen:
                        seen.add(key)
                        result.append(r.name)
            return result

    def _show_summary(self, summary: ImportSummary) -> None:
        lines = [
            f"Rows read: {summary.total_rows}  ·  "
            f"Valid names: {summary.valid_names}  ·  "
            f"Imported: {summary.imported}  ·  "
            f"Skipped: {summary.duplicates_skipped}"
        ]
        self._summary_label.setText("  ".join(lines))
        self._preview_section.setVisible(False)
        self._summary_section.setVisible(True)

    def _show_error(self, message: str) -> None:
        self._error_label.setText(f"⚠  {message}")
        self._error_label.setVisible(True)

    def _hide_error(self) -> None:
        self._error_label.setText("")
        self._error_label.setVisible(False)

    def _reset(self) -> None:
        """Return the view to its initial empty state."""
        self._parse_result = None
        self._preview_rows = []
        self._csv_path = None
        self._file_label.setText("No file selected.")
        self._csv_column_row.setVisible(False)
        self._csv_column_combo.clear()
        self._paste_area.clear()
        self._table.setRowCount(0)
        self._preview_section.setVisible(False)
        self._summary_section.setVisible(False)
        self._hide_error()
        self._skip_radio.setChecked(True)
