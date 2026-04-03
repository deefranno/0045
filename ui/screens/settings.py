from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Settings</h1>"))
        layout.addWidget(QLabel("Placeholder message: This screen will manage application configurations."))
