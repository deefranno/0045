"""
Dashboard – live summary of the product image workflow.
Shows total, approved, pending, and downloaded counts from SQLite.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from core.models import APPROVED_STATUSES, PENDING_STATUSES
from core.repository import ProductRepository


class DashboardView(QWidget):
    def __init__(self, repo: ProductRepository, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._repo = repo
        self._stat_cards: dict[str, _StatCard] = {}
        self._last_updated_label: QLabel
        self._build()

    # ── Construction ─────────────────────────────────────────────────────

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(0)

        # Page header
        title = QLabel("Dashboard")
        title.setObjectName("ViewTitle")
        root.addWidget(title)

        root.addSpacing(4)

        subtitle = QLabel(
            "Live overview of your product image workflow — counts update each time you visit."
        )
        subtitle.setObjectName("ViewSubtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        root.addSpacing(28)

        # Stat cards row
        cards_row = QWidget()
        cards_layout = QHBoxLayout(cards_row)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(16)

        card_specs = [
            ("total",      "Total Products", "#2B5278"),
            ("approved",   "Approved",        "#2E7D4F"),
            ("pending",    "Pending",         "#7A5C1E"),
            ("downloaded", "Downloaded",      "#5C3A8A"),
        ]
        for key, label, accent in card_specs:
            card = _StatCard(label, accent)
            self._stat_cards[key] = card
            cards_layout.addWidget(card)

        root.addWidget(cards_row)
        root.addSpacing(20)

        # Footer: refresh button + last-updated timestamp
        footer = QWidget()
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(12)

        refresh_btn = QPushButton("↻  Refresh")
        refresh_btn.setObjectName("SecondaryButton")
        refresh_btn.setFixedWidth(110)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh)

        self._last_updated_label = QLabel("")
        self._last_updated_label.setObjectName("TimestampLabel")

        footer_layout.addWidget(refresh_btn)
        footer_layout.addStretch()
        footer_layout.addWidget(self._last_updated_label)

        root.addWidget(footer)
        root.addStretch()

        self._apply_extra_styles()

    # ── Data refresh ──────────────────────────────────────────────────────

    def refresh(self) -> None:
        """Re-query the database and update all stat cards."""
        counts = self._repo.get_status_counts()

        total = sum(counts.values())
        approved = sum(counts.get(s, 0) for s in APPROVED_STATUSES)
        pending = sum(counts.get(s, 0) for s in PENDING_STATUSES)
        downloaded = counts.get("downloaded", 0)

        self._stat_cards["total"].set_value(total)
        self._stat_cards["approved"].set_value(approved)
        self._stat_cards["pending"].set_value(pending)
        self._stat_cards["downloaded"].set_value(downloaded)

        ts = datetime.now().strftime("%H:%M:%S")
        self._last_updated_label.setText(f"Last updated: {ts}")

    # ── Styles ────────────────────────────────────────────────────────────

    def _apply_extra_styles(self) -> None:
        self.setStyleSheet(
            self.styleSheet()
            + """
            QPushButton#SecondaryButton {
                background-color: #FFFFFF;
                color: #2B5278;
                border: 1px solid #C8D4E0;
                border-radius: 5px;
                font-size: 13px;
                padding: 5px 12px;
            }
            QPushButton#SecondaryButton:hover {
                background-color: #EEF4FB;
                border-color: #2B5278;
            }
            QLabel#TimestampLabel {
                font-size: 12px;
                color: #9AAABB;
            }
            """
        )


class _StatCard(QFrame):
    """Single metric card: large number + label."""

    def __init__(self, label: str, accent_color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._accent = accent_color
        self.setObjectName("StatCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self._value_label = QLabel("0")
        self._value_label.setObjectName("StatValue")

        self._text_label = QLabel(label)
        self._text_label.setObjectName("StatLabel")

        layout.addWidget(self._value_label)
        layout.addWidget(self._text_label)

        self._apply_card_style()

    def set_value(self, value: int) -> None:
        self._value_label.setText(str(value))

    def _apply_card_style(self) -> None:
        self.setStyleSheet(
            f"""
            QFrame#StatCard {{
                background-color: #FFFFFF;
                border: 1px solid #DDE1E7;
                border-left: 4px solid {self._accent};
                border-radius: 8px;
            }}
            QLabel#StatValue {{
                font-size: 32px;
                font-weight: 700;
                color: {self._accent};
            }}
            QLabel#StatLabel {{
                font-size: 12px;
                font-weight: 600;
                color: #7A8A9A;
                letter-spacing: 0.5px;
            }}
            """
        )
