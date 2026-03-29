"""
BaseView – common scaffold for every section view.
Each concrete view subclasses this and calls super().__init__() with its
title, subtitle, and placeholder icon glyph.  The content area below the
header is exposed via self.content_layout for child classes to populate
in future phases.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt


class BaseView(QWidget):
    """
    Renders:
        ┌─────────────────────────────────────────────────┐
        │  <title>                                        │
        │  <subtitle>                                     │
        ├─────────────────────────────────────────────────┤
        │                                                 │
        │   [placeholder card shown until phase lands]   │
        │                                                 │
        └─────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        title: str,
        subtitle: str,
        placeholder_icon: str = "◫",
        placeholder_text: str = "This section is not yet implemented.",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(0)

        # ── Page header ──────────────────────────────────────────────────
        title_label = QLabel(title)
        title_label.setObjectName("ViewTitle")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("ViewSubtitle")
        subtitle_label.setWordWrap(True)

        root.addWidget(title_label)
        root.addSpacing(4)
        root.addWidget(subtitle_label)
        root.addSpacing(24)

        # ── Content area (subclasses add widgets here) ───────────────────
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(12)

        # Placeholder card — subclasses can remove or replace this
        placeholder = self._build_placeholder(placeholder_icon, placeholder_text)
        self.content_layout.addWidget(placeholder)
        self.content_layout.addStretch()

        root.addWidget(content_widget, 1)

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _build_placeholder(icon: str, text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("PlaceholderCard")
        card.setFixedHeight(180)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        icon_label = QLabel(icon)
        icon_label.setObjectName("PlaceholderIcon")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_label = QLabel(text)
        text_label.setObjectName("PlaceholderText")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        return card
