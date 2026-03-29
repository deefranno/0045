"""
MainWindow – top-level application window.
Composes the header, sidebar, stacked view area, and status bar.
Accepts a ProductRepository so data-aware views can be populated.
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
from core.repository import ProductRepository
from ui.sidebar import Sidebar
from ui.views.dashboard import DashboardView
from ui.views.import_products import ImportProductsView
from ui.views.search_queue import SearchQueueView
from ui.views.review_images import ReviewImagesView
from ui.views.exports import ExportsView
from ui.views.settings import SettingsView


class MainWindow(QMainWindow):
    def __init__(self, repo: ProductRepository) -> None:
        super().__init__()
        self._repo = repo
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self.resize(APP_DEFAULT_WIDTH, APP_DEFAULT_HEIGHT)

        self._views: dict[str, QWidget] = {}
        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────────

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("CentralWidget")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_header())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self._stack = QStackedWidget()
        self._stack.setObjectName("ViewContainer")

        # Instantiate views — data-aware views receive the repository
        view_instances: list[tuple[str, QWidget]] = [
            ("Dashboard",       DashboardView(self._repo)),
            ("Import Products", ImportProductsView()),
            ("Search Queue",    SearchQueueView()),
            ("Review Images",   ReviewImagesView()),
            ("Exports",         ExportsView()),
            ("Settings",        SettingsView()),
        ]
        for section, view in view_instances:
            self._views[section] = view
            self._stack.addWidget(view)

        self._sidebar = Sidebar()
        self._sidebar.navigation_changed.connect(self._on_nav_changed)

        body_layout.addWidget(self._sidebar)
        body_layout.addWidget(self._stack, stretch=1)

        root_layout.addWidget(body, stretch=1)

        self._status_bar = QStatusBar()
        self._status_bar.showMessage("Ready")
        self.setStatusBar(self._status_bar)

        # Trigger initial nav + first data refresh
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
        if view is None:
            return
        self._stack.setCurrentWidget(view)
        self._status_bar.showMessage(f"Section: {section}")
        # Refresh data if the view supports it (duck-typed, no forced base class)
        if hasattr(view, "refresh"):
            view.refresh()
