import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTabWidget, QFileDialog, QTableWidget,
    QTableWidgetItem, QComboBox, QPlainTextEdit,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from core import importer
from utils.logger import logger

class ImportScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = pd.DataFrame()
        self.column_names = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title_label = QLabel("Import Products")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Tab 1: Upload CSV
        self.csv_tab = QWidget()
        self.setup_csv_tab()
        self.tabs.addTab(self.csv_tab, "Upload CSV")

        # Tab 2: Manual Entry
        self.manual_tab = QWidget()
        self.setup_manual_tab()
        self.tabs.addTab(self.manual_tab, "Paste / Manual Entry")

        # Preview Section (shared)
        preview_label = QLabel("Data Preview (Top 50)")
        layout.addWidget(preview_label)

        self.preview_table = QTableWidget()
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.preview_table)

        # Feedback label
        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

    def setup_csv_tab(self):
        layout = QVBoxLayout(self.csv_tab)

        # File selector
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        choose_file_btn = QPushButton("Choose CSV File")
        choose_file_btn.clicked.connect(self.on_choose_file)
        file_layout.addWidget(choose_file_btn)
        file_layout.addWidget(self.file_path_label)
        file_layout.addStretch()
        layout.addLayout(file_layout)

        # Column mapping
        mapping_group = QWidget()
        mapping_layout = QVBoxLayout(mapping_group)

        self.mapping_combos = {}
        fields = [("product_name", "Product Name (required)"), ("sku", "SKU"), ("brand", "Brand")]

        for key, label_text in fields:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            combo = QComboBox()
            combo.addItem("-- ignore --")
            self.mapping_combos[key] = combo
            row.addWidget(combo)
            mapping_layout.addLayout(row)

        layout.addWidget(mapping_group)

        # Action button
        import_btn = QPushButton("Validate & Import")
        import_btn.clicked.connect(self.on_import_csv)
        layout.addWidget(import_btn)
        layout.addStretch()

    def setup_manual_tab(self):
        layout = QVBoxLayout(self.manual_tab)

        layout.addWidget(QLabel("Product Names (one per line):"))
        self.manual_text = QPlainTextEdit()
        layout.addWidget(self.manual_text)

        sku_layout = QHBoxLayout()
        sku_layout.addWidget(QLabel("SKU Prefix (optional):"))
        self.sku_prefix = QLineEdit()
        sku_layout.addWidget(self.sku_prefix)
        layout.addLayout(sku_layout)

        import_manual_btn = QPushButton("Import Lines")
        import_manual_btn.clicked.connect(self.on_import_manual)
        layout.addWidget(import_manual_btn)

    def on_choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path_label.setText(file_path)
            self.df, self.column_names = importer.parse_csv(file_path)

            if self.df.empty:
                QMessageBox.warning(self, "Parse Error", "Failed to parse CSV file or file is empty.")
                return

            self.update_preview()
            self.update_combos()

    def update_combos(self):
        for combo in self.mapping_combos.values():
            combo.clear()
            combo.addItem("-- ignore --")
            combo.addItems(self.column_names)

            # Auto-match logic (optional, for convenience)
            for i in range(combo.count()):
                text = combo.itemText(i).lower()
                # Simple matching logic
                if "name" in text or "product" in text:
                    if combo == self.mapping_combos["product_name"]:
                        combo.setCurrentIndex(i)
                elif "sku" in text:
                    if combo == self.mapping_combos["sku"]:
                        combo.setCurrentIndex(i)
                elif "brand" in text:
                    if combo == self.mapping_combos["brand"]:
                        combo.setCurrentIndex(i)

    def update_preview(self):
        self.preview_table.clear()
        if self.df.empty:
            self.preview_table.setRowCount(0)
            self.preview_table.setColumnCount(0)
            return

        preview_df = self.df.head(50)
        self.preview_table.setRowCount(len(preview_df))
        self.preview_table.setColumnCount(len(preview_df.columns))
        self.preview_table.setHorizontalHeaderLabels(preview_df.columns)

        for i, row in preview_df.iterrows():
            for j, val in enumerate(row):
                self.preview_table.setItem(i, j, QTableWidgetItem(str(val)))

    def on_import_csv(self):
        if self.df.empty:
            QMessageBox.warning(self, "Error", "Please choose a CSV file first.")
            return

        mapping = {k: v.currentText() for k, v in self.mapping_combos.items()}
        errors = importer.validate_mapping(self.df, mapping)

        if errors:
            self.feedback_label.setText("\n".join(errors))
            self.feedback_label.setStyleSheet("color: red;")
            return

        try:
            saved, empty, duplicate = importer.save_products(self.df, mapping)
            self.feedback_label.setText(f"Success: {saved} imported, {empty} empty, {duplicate} duplicates.")
            self.feedback_label.setStyleSheet("color: green;")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def on_import_manual(self):
        lines = self.manual_text.toPlainText().splitlines()
        product_names = [line.strip() for line in lines if line.strip()]

        if not product_names:
            QMessageBox.warning(self, "Error", "Please enter at least one product name.")
            return

        sku_prefix = self.sku_prefix.text().strip()
        data = []
        for i, name in enumerate(product_names):
            sku = f"{sku_prefix}{i+1:04d}" if sku_prefix else None
            data.append({"product_name": name, "sku": sku, "brand": None})

        df_manual = pd.DataFrame(data)
        mapping = {"product_name": "product_name", "sku": "sku", "brand": "brand"}

        try:
            saved, empty, duplicate = importer.save_products(df_manual, mapping)
            self.feedback_label.setText(f"Success: {saved} products imported manually.")
            self.feedback_label.setStyleSheet("color: green;")
            self.manual_text.clear()
            self.df = df_manual
            self.update_preview()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
