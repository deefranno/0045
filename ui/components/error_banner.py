from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer

class ErrorBanner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: #f39c12; color: white;")
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.message_label = QLabel("")
        self.layout.addWidget(self.message_label)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedWidth(30)
        self.close_btn.clicked.connect(self.clear)
        self.layout.addWidget(self.close_btn)

        self.hide()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clear)

    def show_error(self, message: str):
        self.message_label.setText(message)
        self.show()
        self.timer.start(8000)

    def clear(self):
        self.hide()
