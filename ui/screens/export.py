import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QRadioButton, QButtonGroup, QFileDialog,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from core import exporter
from utils.logger import logger

class ExportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = pd.DataFrame()
        self.export_path = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Export Results")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Filter controls
        filter_group = QWidget()
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.addWidget(QLabel("Export scope:"))

        self.btn_group = QButtonGroup(self)
        self.radio_accepted = QRadioButton("Accepted only")
        self.radio_accepted.setChecked(True)
        self.radio_all = QRadioButton("All results")
        self.radio_no_match = QRadioButton("No matches only")

        for rb in [self.radio_accepted, self.radio_all, self.radio_no_match]:
            self.btn_group.addButton(rb)
            filter_layout.addWidget(rb)
            rb.clicked.connect(self.load_preview)

        layout.addWidget(filter_group)

        # Preview Section
        self.row_count_label = QLabel("0 rows ready for export")
        layout.addWidget(self.row_count_label)

        self.preview_table = QTableWidget()
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.preview_table)

        # Bottom Section
        bottom_layout = QVBoxLayout()

        file_path_layout = QHBoxLayout()
        self.btn_choose_path = QPushButton("Choose Export Location")
        self.btn_choose_path.clicked.connect(self.on_choose_path)
        file_path_layout.addWidget(self.btn_choose_path)

        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        file_path_layout.addWidget(self.path_input)
        bottom_layout.addLayout(file_path_layout)

        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self.on_export)
        bottom_layout.addWidget(self.btn_export)

        layout.addLayout(bottom_layout)

        # Feedback label
        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        # Initial preview load
        self.load_preview()

    def load_preview(self):
        status_map = {
            self.radio_accepted: "accepted",
            self.radio_all: "all",
            self.radio_no_match: "no_match"
        }
        status_filter = status_map[self.btn_group.checkedButton()]

        self.df = exporter.build_export_dataframe(status_filter)
        self.row_count_label.setText(f"{len(self.df)} rows ready for export")

        # Table Preview (top 20)
        preview_df = self.df.head(20)
        self.preview_table.setRowCount(len(preview_df))
        self.preview_table.setColumnCount(len(preview_df.columns))
        self.preview_table.setHorizontalHeaderLabels(preview_df.columns)

        for i, row in preview_df.iterrows():
            for j, val in enumerate(row):
                self.preview_table.setItem(i, j, QTableWidgetItem(str(val)))

    def on_choose_path(self):
        default_name = f"product_images_{QDate.currentDate().toString('yyyy-MM-dd')}.csv"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Choose Export Location", default_name, "CSV Files (*.csv)"
        )
        if file_path:
            self.export_path = file_path
            self.path_input.setText(file_path)
            self.btn_export.setEnabled(True)

    def on_export(self):
        if not self.export_path: return

        success, error = exporter.export_to_csv(self.df, self.export_path)
        if success:
            self.feedback_label.setText(f"Export complete — {len(self.df)} rows written to {self.export_path}")
            self.feedback_label.setStyleSheet("color: green;")
        else:
            QMessageBox.critical(self, "Export Failed", f"Error: {error}")
