"""
Left-side navigation sidebar.
Emits navigation_changed(section_name) when the user switches sections.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy,
)
from PySide6.QtCore import Signal, Qt

from core.config import SIDEBAR_WIDTH, NAV_SECTIONS, NAV_GLYPHS


class Sidebar(QWidget):
    """Vertical navigation panel with checkable section buttons."""

    navigation_changed: Signal = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self._buttons: dict[str, QPushButton] = {}
        self._build()

    # ── Construction ─────────────────────────────────────────────────────

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(2)

        # Section label above the nav items
        group_label = QLabel("NAVIGATION")
        group_label.setObjectName("NavGroupLabel")
        group_label.setContentsMargins(20, 0, 0, 10)
        group_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(group_label)

        for section in NAV_SECTIONS:
            btn = self._make_nav_button(section)
            self._buttons[section] = btn
            layout.addWidget(btn)

        # Push everything upward; settings naturally sits at bottom via order
        layout.addStretch()

    def _make_nav_button(self, section: str) -> QPushButton:
        glyph = NAV_GLYPHS.get(section, "•")
        btn = QPushButton(f"  {glyph}   {section}")
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setFixedHeight(42)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # Use default arg capture to avoid late-binding closure bug
        btn.clicked.connect(lambda _checked, s=section: self.select(s))
        return btn

    # ── Public API ────────────────────────────────────────────────────────

    def select(self, section: str) -> None:
        """Activate a navigation item programmatically or on click."""
        for name, btn in self._buttons.items():
            btn.setChecked(name == section)
        self.navigation_changed.emit(section)

    def select_default(self) -> None:
        """Select the first section on startup."""
        if NAV_SECTIONS:
            self.select(NAV_SECTIONS[0])
