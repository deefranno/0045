"""
MainWindow – top-level application window.
Composes the header, sidebar, stacked view area, and status bar.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QStatusBar, QLabel, QFrame,
)
from PySide6.QtCore import Qt

from core.config import (
    APP_NAME, APP_VERSION,
    APP_MIN_WIDTH, APP_MIN_HEIGHT,
    APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT,
    NAV_SECTIONS,
)
from ui.sidebar import Sidebar
from ui.views.dashboard import DashboardView
from ui.views.import_products import ImportProductsView
from ui.views.search_queue import SearchQueueView
from ui.views.review_images import ReviewImagesView
from ui.views.exports import ExportsView
from ui.views.settings import SettingsView


# Maps section name → view class (order must match NAV_SECTIONS)
_VIEW_CLASSES = {
    "Dashboard":       DashboardView,
    "Import Products": ImportProductsView,
    "Search Queue":    SearchQueueView,
    "Review Images":   ReviewImagesView,
    "Exports":         ExportsView,
    "Settings":        SettingsView,
}


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME}")
        self.setMinimumSize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self.resize(APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT)

        self._views: dict[str, QWidget] = {}
        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Root widget replaces the bare QMainWindow background
        root = QWidget()
        root.setObjectName("CentralWidget")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1 – Fixed header bar
        root_layout.addWidget(self._build_header())

        # 2 – Body: sidebar + stacked content
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._stack = QStackedWidget()
        self._stack.setObjectName("ViewContainer")

        # Instantiate views in NAV_SECTIONS order so indices stay stable
        for section in NAV_SECTIONS:
            view_cls = _VIEW_CLASSES[section]
            view = view_cls()
            self._views[section] = view
            self._stack.addWidget(view)

        self._sidebar = Sidebar()
        self._sidebar.navigation_changed.connect(self._on_nav_changed)

        body_layout.addWidget(self._sidebar)
        body_layout.addWidget(self._stack, stretch=1)

        root_layout.addWidget(body, stretch=1)

        # 3 – Status bar (QMainWindow native)
        self._status_bar = QStatusBar()
        self._status_bar.showMessage("Ready")
        self.setStatusBar(self._status_bar)

        # Activate the default section
        self._sidebar.select_default()

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("AppHeader")
        header.setFixedHeight(52)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel(APP_NAME)
        title.setObjectName("AppTitle")

        version = QLabel(f"v{APP_VERSION}")
        version.setObjectName("AppVersion")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(version)

        return header

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_nav_changed(self, section: str) -> None:
        view = self._views.get(section)
        if view is not None:
            self._stack.setCurrentWidget(view)
            self._status_bar.showMessage(f"Section: {section}")
