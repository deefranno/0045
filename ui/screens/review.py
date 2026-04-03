import httpx
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem,
    QScrollArea, QFrame, QLineEdit, QMessageBox,
    QButtonGroup, QRadioButton
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize
from PySide6.QtGui import QPixmap, QImage
from core import review_store
from utils.logger import logger
import json

class ThumbnailLoader(QThread):
    loaded = Signal(int, QPixmap)
    failed = Signal(int)

    def __init__(self, index, url):
        super().__init__()
        self.index = index
        self.url = url

    def run(self):
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(self.url)
                if resp.status_code == 200:
                    image = QImage()
                    image.loadFromData(resp.content)
                    if not image.isNull():
                        pixmap = QPixmap.fromImage(image)
                        self.loaded.emit(self.index, pixmap)
                    else:
                        self.failed.emit(self.index)
                else:
                    self.failed.emit(self.index)
        except Exception as e:
            logger.error(f"Thumbnail load failed for {self.url}: {e}")
            self.failed.emit(self.index)

class ReviewScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.products = []
        self.current_product = None
        self.selected_thumbnail_url = None
        self.loaders = []
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # Left Panel — Product Queue
        left_panel = QFrame()
        left_panel.setFixedWidth(280)
        left_layout = QVBoxLayout(left_panel)

        # Filter buttons
        filter_group = QWidget()
        filter_layout = QHBoxLayout(filter_group)
        self.btn_group = QButtonGroup(self)

        for status in ["Pending", "Accepted", "Rejected"]:
            btn = QRadioButton(status)
            if status == "Pending": btn.setChecked(True)
            self.btn_group.addButton(btn)
            filter_layout.addWidget(btn)

        self.btn_group.buttonClicked.connect(self.load_data)
        left_layout.addWidget(filter_group)

        self.product_list = QListWidget()
        self.product_list.currentRowChanged.connect(self.on_product_selected)
        left_layout.addWidget(self.product_list)

        main_layout.addWidget(left_panel)

        # Right Panel — Review Detail
        self.right_panel = QFrame()
        right_layout = QVBoxLayout(self.right_panel)

        self.heading = QLabel("Select a product to review")
        self.heading.setStyleSheet("font-size: 18px; font-weight: bold;")
        right_layout.addWidget(self.heading)

        self.score_label = QLabel("")
        right_layout.addWidget(self.score_label)

        self.explanation_label = QLabel("")
        self.explanation_label.setWordWrap(True)
        right_layout.addWidget(self.explanation_label)

        # Candidate image strip
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(200)
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)
        self.scroll_area.setWidget(self.image_container)
        right_layout.addWidget(self.scroll_area)

        # Action bar
        action_bar = QWidget()
        action_layout = QHBoxLayout(action_bar)

        self.btn_accept = QPushButton("Accept (A)")
        self.btn_accept.clicked.connect(self.on_accept)
        action_layout.addWidget(self.btn_accept)

        self.btn_reject = QPushButton("Reject (R)")
        self.btn_reject.clicked.connect(self.on_reject)
        action_layout.addWidget(self.btn_reject)

        self.btn_no_match = QPushButton("No Match (N)")
        self.btn_no_match.clicked.connect(self.on_no_match)
        action_layout.addWidget(self.btn_no_match)

        right_layout.addWidget(action_bar)

        # Custom URL
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Custom URL:"))
        self.custom_url_input = QLineEdit()
        custom_layout.addWidget(self.custom_url_input)
        btn_use_custom = QPushButton("Use This")
        btn_use_custom.clicked.connect(self.on_use_custom)
        custom_layout.addWidget(btn_use_custom)
        right_layout.addLayout(custom_layout)

        main_layout.addWidget(self.right_panel)

        # Initial load
        self.load_data()

    def load_data(self):
        status_map = {"Pending": "pending_review", "Accepted": "accepted", "Rejected": "rejected"}
        selected_text = self.btn_group.checkedButton().text()
        db_status = status_map[selected_text]

        self.products = review_store.get_pending_products(db_status)
        self.product_list.clear()

        for p in self.products:
            name = p.get('cleaned_name') or p.get('raw_name')
            score = p.get('confidence', 0)
            item = QListWidgetItem(f"{name} ({score})")

            # Badge colour
            if score >= 85: item.setForeground(Qt.green)
            elif score >= 60: item.setForeground(Qt.yellow)
            else: item.setForeground(Qt.red)

            self.product_list.addItem(item)

        if not self.products:
            self.heading.setText("Queue complete")
            self.right_panel.setEnabled(False)
        else:
            self.right_panel.setEnabled(True)

    def on_product_selected(self, index):
        if index < 0 or index >= len(self.products): return

        self.current_product = self.products[index]
        p = self.current_product

        self.heading.setText(p.get('cleaned_name') or p.get('raw_name'))
        self.score_label.setText(f"Score: {p.get('confidence', 0)}")

        expl = p.get('explanation', "[]")
        try:
            expl_list = json.loads(expl)
            self.explanation_label.setText("\n".join([f"• {e}" for e in expl_list]))
        except:
            self.explanation_label.setText(expl)

        self.clear_thumbnails()
        self.load_thumbnails(p.get('candidates', []))

    def clear_thumbnails(self):
        for loader in self.loaders:
            loader.terminate()
        self.loaders = []

        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

    def load_thumbnails(self, candidates):
        self.thumbnail_widgets = []
        for i, cand in enumerate(candidates[:8]):
            frame = QFrame()
            frame.setFixedSize(130, 160)
            layout = QVBoxLayout(frame)

            img_label = QLabel("Loading...")
            img_label.setFixedSize(120, 120)
            img_label.setStyleSheet("background-color: grey;")
            img_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(img_label)

            domain_label = QLabel(cand.get('domain', ''))
            domain_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(domain_label)

            self.image_layout.addWidget(frame)
            self.thumbnail_widgets.append((img_label, cand['image_url']))

            loader = ThumbnailLoader(i, cand['image_url'])
            loader.loaded.connect(self.on_thumbnail_loaded)
            loader.failed.connect(self.on_thumbnail_failed)
            loader.start()
            self.loaders.append(loader)

            # Clickable frame (pseudo-implementation)
            frame.mousePressEvent = lambda e, url=cand['image_url'], f=frame: self.on_thumbnail_clicked(url, f)

    @Slot(int, QPixmap)
    def on_thumbnail_loaded(self, index, pixmap):
        label, _ = self.thumbnail_widgets[index]
        label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @Slot(int)
    def on_thumbnail_failed(self, index):
        label, _ = self.thumbnail_widgets[index]
        label.setText("unavailable")

    def on_thumbnail_clicked(self, url, frame):
        self.selected_thumbnail_url = url
        # Highlight border
        for i in range(self.image_layout.count()):
            w = self.image_layout.itemAt(i).widget()
            w.setStyleSheet("")
        frame.setStyleSheet("border: 2px solid blue;")

    def on_accept(self):
        if not self.current_product or not self.selected_thumbnail_url:
            QMessageBox.warning(self, "Error", "Please select an image first.")
            return
        self.save_and_advance("accepted", self.selected_thumbnail_url)

    def on_reject(self):
        if not self.current_product: return
        self.save_and_advance("rejected", None)

    def on_no_match(self):
        if not self.current_product: return
        self.save_and_advance("no_match", None)

    def on_use_custom(self):
        url = self.custom_url_input.text().strip()
        if not url: return
        self.save_and_advance("accepted", url)

    def save_and_advance(self, status, url):
        try:
            review_store.save_decision(self.current_product['id'], status, url)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A: self.on_accept()
        elif event.key() == Qt.Key_R: self.on_reject()
        elif event.key() == Qt.Key_N: self.on_no_match()
        elif event.key() == Qt.Key_Left:
            self.product_list.setCurrentRow(max(0, self.product_list.currentRow() - 1))
        elif event.key() == Qt.Key_Right:
            self.product_list.setCurrentRow(min(self.product_list.count() - 1, self.product_list.currentRow() + 1))
        elif Qt.Key_1 <= event.key() <= Qt.Key_8:
            idx = event.key() - Qt.Key_1
            if idx < len(self.thumbnail_widgets):
                _, url = self.thumbnail_widgets[idx]
                frame = self.image_layout.itemAt(idx).widget()
                self.on_thumbnail_clicked(url, frame)
        super().keyPressEvent(event)
