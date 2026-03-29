"""
Search Queue view.

Shows products with status 'new', 'cleaned', or 'error'.
Lets the operator:
  - Auto-clean all 'new' products with the cleaning engine
  - Clean only selected rows
  - Manually edit any cleaned name inline (double-click the cell)

The Cleaned Name column is the only editable column.
Edits are saved to the database immediately on cell commit.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.cleaner import clean, clean_batch
from core.models import Product
from core.repository import ProductRepository

logger = logging.getLogger(__name__)

# Statuses shown in this queue (products awaiting search)
_QUEUE_STATUSES = ["new", "cleaned", "error"]

# Table column indices
_COL_NUM      = 0   # row counter; product_id stored in UserRole
_COL_ORIGINAL = 1   # original_name  — not editable
_COL_CLEANED  = 2   # cleaned_name   — editable
_COL_STATUS   = 3   # status         — not editable

# Foreground colours per status
_STATUS_FG: dict[str, QColor] = {
    "new":     QColor("#8A9BB0"),
    "cleaned": QColor("#2B5278"),
    "error":   QColor("#B22222"),
}
_DEFAULT_FG = QColor("#1C2B3A")


class SearchQueueView(QWidget):
    def __init__(self, repo: ProductRepository, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._repo = repo
        self._products: list[Product] = []

        # Widgets set during _build
        self._clean_new_btn: QPushButton
        self._clean_selected_btn: QPushButton
        self._stats_label: QLabel
        self._table: QTableWidget

        self._build()

    # ── Construction ──────────────────────────────────────────────────────

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 20)
        root.setSpacing(0)

        # Header
        title = QLabel("Search Queue")
        title.setObjectName("ViewTitle")
        root.addWidget(title)
        root.addSpacing(4)

        subtitle = QLabel(
            "Review and clean product names before running image searches. "
            "Double-click a Cleaned Name cell to edit it manually."
        )
        subtitle.setObjectName("ViewSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)
        root.addSpacing(20)

        # Action bar
        root.addWidget(self._build_action_bar())
        root.addSpacing(10)

        # Product table
        root.addWidget(self._build_table(), stretch=1)
        root.addSpacing(4)

        # Footer hint
        hint = QLabel("Tip: select rows with Ctrl+click or Shift+click, then use Clean Selected.")
        hint.setObjectName("TableHint")
        root.addWidget(hint)

    def _build_action_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("ActionBar")
        bar.setFixedHeight(52)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(10)

        self._clean_new_btn = QPushButton("Clean All New (0)")
        self._clean_new_btn.setObjectName("SecondaryButton")
        self._clean_new_btn.setFixedWidth(160)
        self._clean_new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clean_new_btn.setEnabled(False)
        self._clean_new_btn.clicked.connect(self._on_clean_all_new)

        self._clean_selected_btn = QPushButton("Clean Selected")
        self._clean_selected_btn.setObjectName("SecondaryButton")
        self._clean_selected_btn.setFixedWidth(130)
        self._clean_selected_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clean_selected_btn.setEnabled(False)
        self._clean_selected_btn.clicked.connect(self._on_clean_selected)

        refresh_btn = QPushButton("↺  Refresh")
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.setFixedWidth(100)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh)

        self._stats_label = QLabel("")
        self._stats_label.setObjectName("StatsLabel")

        layout.addWidget(self._clean_new_btn)
        layout.addWidget(self._clean_selected_btn)
        layout.addWidget(refresh_btn)
        layout.addStretch()
        layout.addWidget(self._stats_label)

        return bar

    def _build_table(self) -> QTableWidget:
        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["#", "Original Name", "Cleaned Name", "Status"])

        # Column sizing
        table.horizontalHeader().setSectionResizeMode(
            _COL_NUM, QHeaderView.ResizeMode.Fixed
        )
        table.horizontalHeader().setSectionResizeMode(
            _COL_ORIGINAL, QHeaderView.ResizeMode.Stretch
        )
        table.horizontalHeader().setSectionResizeMode(
            _COL_CLEANED, QHeaderView.ResizeMode.Stretch
        )
        table.horizontalHeader().setSectionResizeMode(
            _COL_STATUS, QHeaderView.ResizeMode.Fixed
        )
        table.setColumnWidth(_COL_NUM, 52)
        table.setColumnWidth(_COL_STATUS, 100)

        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setAlternatingRowColors(False)

        # Editing: only Cleaned Name column; other columns have ItemIsEditable
        # flag absent (set per-item during population)
        table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        # Signals
        table.itemChanged.connect(self._on_item_changed)
        table.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self._table = table
        return table

    # ── Public API ────────────────────────────────────────────────────────

    def refresh(self) -> None:
        """Reload products from the database and repopulate the table."""
        self._products = self._repo.get_products_by_statuses(_QUEUE_STATUSES)
        self._update_stats()
        self._populate_table()

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_clean_all_new(self) -> None:
        new_products = [p for p in self._products if p.status == "new"]
        if not new_products:
            return

        results = clean_batch([p.original_name for p in new_products])
        updates = [
            (p.id, r.cleaned)
            for p, r in zip(new_products, results)
            if p.id is not None
        ]
        self._repo.batch_update_cleaned_names(updates)
        logger.info("Cleaned %d products", len(updates))

        self.refresh()
        self._show_clean_summary(new_products, results)

    def _on_clean_selected(self) -> None:
        selected_rows = {index.row() for index in self._table.selectedIndexes()}
        if not selected_rows:
            return

        updates: list[tuple[int, str]] = []
        for row in sorted(selected_rows):
            num_item = self._table.item(row, _COL_NUM)
            orig_item = self._table.item(row, _COL_ORIGINAL)
            if num_item is None or orig_item is None:
                continue
            product_id: int = num_item.data(Qt.ItemDataRole.UserRole)
            cleaned_name = clean(orig_item.text())
            updates.append((product_id, cleaned_name))

        if updates:
            self._repo.batch_update_cleaned_names(updates)
            logger.info("Cleaned %d selected products", len(updates))
            self.refresh()

    def _on_item_changed(self, item: QTableWidgetItem) -> None:
        """Auto-save when the user commits a manual edit to the Cleaned Name column."""
        if item.column() != _COL_CLEANED:
            return
        # Guard: only process user edits, not programmatic changes during populate
        if not item.flags() & Qt.ItemFlag.ItemIsEditable:
            return

        row = item.row()
        num_item = self._table.item(row, _COL_NUM)
        if num_item is None:
            return

        product_id: int = num_item.data(Qt.ItemDataRole.UserRole)
        new_name = item.text().strip()
        if not new_name:
            return  # don't save an empty cleaned name

        self._repo.update_cleaned_name(product_id, new_name)
        logger.debug("Manual edit saved: id=%s → %r", product_id, new_name)

        # Update the status column in the table to reflect possible status change
        self._refresh_status_cell(row, product_id)

    def _on_selection_changed(self) -> None:
        has_selection = bool(self._table.selectedItems())
        self._clean_selected_btn.setEnabled(has_selection)

    # ── Helpers ───────────────────────────────────────────────────────────

    def _populate_table(self) -> None:
        # Block signals so programmatic cell writes don't trigger _on_item_changed
        self._table.blockSignals(True)
        self._table.setRowCount(0)
        self._table.setRowCount(len(self._products))

        for i, product in enumerate(self._products):
            # Col 0: row number — stores product_id in UserRole
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            num_item.setForeground(QColor("#9AAABB"))
            num_item.setData(Qt.ItemDataRole.UserRole, product.id)
            num_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            # Col 1: original name — read-only
            orig_item = QTableWidgetItem(product.original_name)
            orig_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            # Col 2: cleaned name — editable
            cleaned_text = product.cleaned_name or ""
            cleaned_item = QTableWidgetItem(cleaned_text)
            if not cleaned_text:
                cleaned_item.setForeground(QColor("#C0CCD8"))
            cleaned_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsEditable
            )

            # Col 3: status badge — read-only
            status_item = QTableWidgetItem(product.status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(_STATUS_FG.get(product.status, _DEFAULT_FG))
            status_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self._table.setItem(i, _COL_NUM, num_item)
            self._table.setItem(i, _COL_ORIGINAL, orig_item)
            self._table.setItem(i, _COL_CLEANED, cleaned_item)
            self._table.setItem(i, _COL_STATUS, status_item)

        self._table.resizeRowsToContents()
        self._table.blockSignals(False)

    def _refresh_status_cell(self, row: int, product_id: int) -> None:
        """Re-read a single product's status from the DB and update the status cell."""
        product = self._repo.get_by_id(product_id)
        if product is None:
            return
        status_item = self._table.item(row, _COL_STATUS)
        if status_item:
            self._table.blockSignals(True)
            status_item.setText(product.status)
            status_item.setForeground(_STATUS_FG.get(product.status, _DEFAULT_FG))
            self._table.blockSignals(False)

    def _update_stats(self) -> None:
        counts = self._repo.get_status_counts()
        new_count = counts.get("new", 0)
        cleaned_count = counts.get("cleaned", 0)
        total_queue = sum(counts.get(s, 0) for s in _QUEUE_STATUSES)

        self._stats_label.setText(
            f"{new_count} new  ·  {cleaned_count} cleaned  ·  {total_queue} in queue"
        )
        self._clean_new_btn.setText(f"Clean All New ({new_count})")
        self._clean_new_btn.setEnabled(new_count > 0)

    def _show_clean_summary(
        self, products: list[Product], results: list  # list[CleanResult]
    ) -> None:
        changed = [r for r in results if r.changed]
        unchanged = len(results) - len(changed)

        # Build a sample of before/after pairs (first 25)
        sample_lines = [
            f"{r.original}\n  →  {r.cleaned}"
            for r in changed[:25]
        ]
        if len(changed) > 25:
            sample_lines.append(f"… and {len(changed) - 25} more")

        msg = QMessageBox(self)
        msg.setWindowTitle("Clean Complete")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(
            f"<b>{len(changed)}</b> product{'s' if len(changed) != 1 else ''} cleaned."
        )
        msg.setInformativeText(
            f"{unchanged} product{'s' if unchanged != 1 else ''} already had clean names."
        )
        if sample_lines:
            msg.setDetailedText("\n\n".join(sample_lines))
        msg.exec()
