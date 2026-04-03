from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QListWidget, QFrame,
    QLabel, QProgressBar, QStatusBar
)
from PySide6.QtCore import Qt, QSize
from ui.screens.dashboard import DashboardScreen
from ui.screens.import_screen import ImportScreen
from ui.screens.results import ResultsScreen
from ui.screens.review import ReviewScreen
from ui.screens.settings import SettingsScreen
from ui.screens.export import ExportScreen
from ui.components.error_banner import ErrorBanner

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle("Product Image Matcher Pro")
        self.setMinimumSize(1100, 700)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2c3e50; color: white;")
        sidebar_layout = QVBoxLayout(self.sidebar)

        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget { background-color: transparent; border: none; outline: none; }
            QListWidget::item { padding: 15px; color: white; border-bottom: 1px solid #34495e; }
            QListWidget::item:selected { background-color: #3498db; }
        """)

        nav_items = [
            "Dashboard", "Import", "Results", "Review", "Settings", "Export"
        ]
        self.nav_list.addItems(nav_items)
        self.nav_list.currentRowChanged.connect(self.display_screen)
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addStretch()

        # Sidebar container (to include error banner below sidebar)
        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(200)
        sidebar_v_layout = QVBoxLayout(sidebar_container)
        sidebar_v_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_v_layout.setSpacing(0)

        sidebar_v_layout.addWidget(self.sidebar)

        self.error_banner = ErrorBanner()
        sidebar_v_layout.addWidget(self.error_banner)

        main_layout.addWidget(sidebar_container)

        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Screens
        self.screens = [
            DashboardScreen(),
            ImportScreen(),
            ResultsScreen(),
            ReviewScreen(),
            SettingsScreen(),
            ExportScreen()
        ]

        for screen in self.screens:
            self.content_stack.addWidget(screen)

        # Status bar & Progress
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        self.nav_list.setCurrentRow(0)

    def display_screen(self, index):
        self.content_stack.setCurrentIndex(index)

    def set_progress(self, value, message=None):
        self.progress_bar.setValue(value)
        if message:
            self.status_bar.showMessage(message)

    def show_progress(self, visible):
        self.progress_bar.setVisible(visible)
