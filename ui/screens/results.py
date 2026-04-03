from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QProgressBar, QMessageBox
)
from core.worker import SearchWorker
from core.database import get_connection
from utils.logger import logger

class ResultsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Process Results</h1>"))

        # Action bar
        actions = QHBoxLayout()
        self.btn_start = QPushButton("Start Matching Pipeline")
        self.btn_start.clicked.connect(self.on_start_pipeline)
        actions.addWidget(self.btn_start)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.setEnabled(False)
        self.btn_pause.clicked.connect(self.on_pause)
        actions.addWidget(self.btn_pause)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.on_cancel)
        actions.addWidget(self.btn_cancel)

        layout.addLayout(actions)

        # Logs/Status list
        self.status_list = QListWidget()
        layout.addWidget(self.status_list)

        # Local progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

    def on_start_pipeline(self):
        # Get pending products (those without a decision)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM products
            WHERE id NOT IN (SELECT product_id FROM decisions)
        """)
        product_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not product_ids:
            QMessageBox.information(self, "Pipeline", "No pending products found. Import some first!")
            return

        self.status_list.clear()
        self.status_list.addItem(f"Starting pipeline for {len(product_ids)} products...")

        # In a real app, config would be passed from main_window
        # Accessing via parent window if possible
        main_win = self.window()
        config = getattr(main_win, 'config', {})

        self.worker = SearchWorker(product_ids, config)

        # Connect signals
        self.worker.progress.connect(self.on_progress)
        self.worker.status_message.connect(self.on_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)

        # Link to main window progress if available
        if hasattr(main_win, 'set_progress'):
            self.worker.progress.connect(lambda v: main_win.set_progress(v, "Processing..."))
            main_win.show_progress(True)

        self.worker.start()
        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_cancel.setEnabled(True)

    def on_progress(self, value):
        self.progress_bar.setValue(value)

    def on_status(self, message):
        self.status_list.addItem(message)
        self.status_list.scrollToBottom()

    def on_finished(self, results):
        self.status_list.addItem(f"Pipeline finished! Processed {len(results)} products.")
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        self.btn_pause.setText("Pause")

        main_win = self.window()
        if hasattr(main_win, 'show_progress'):
            main_win.show_progress(False)

    def on_error(self, message):
        QMessageBox.critical(self, "Pipeline Error", message)
        self.on_finished([])

    def on_pause(self):
        if not self.worker: return
        if self.btn_pause.text() == "Pause":
            self.worker.pause()
            self.btn_pause.setText("Resume")
            self.status_list.addItem("Pipeline paused.")
        else:
            self.worker.resume()
            self.btn_pause.setText("Pause")
            self.status_list.addItem("Pipeline resumed.")

    def on_cancel(self):
        if not self.worker: return
        self.worker.cancel()
        self.status_list.addItem("Cancelling pipeline...")
        self.btn_cancel.setEnabled(False)
