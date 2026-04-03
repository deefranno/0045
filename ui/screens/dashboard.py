from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DashboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Dashboard</h1>"))
        layout.addWidget(QLabel("Placeholder message: This dashboard will show overview metrics."))
