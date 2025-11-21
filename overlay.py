import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from telemetry_graph import TelemetryGraph
APP_NAME = 'input telemetry'
class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        quit_shortcut = QShortcut(QKeySequence('f6'), self)
        quit_shortcut.activated.connect(self.close)
        self.global_styles = """
            background-color: rgba(0, 255, 0, 150);
            border-radius: 8px;
        """
        self.drag_position = None

        layout = QVBoxLayout()
        self.drag_handle = QWidget()
        self.drag_handle.setFixedHeight(30)
        self.drag_handle.setSizePolicy(
            self.drag_handle.sizePolicy().horizontalPolicy(),
            self.drag_handle.sizePolicy().verticalPolicy()
        )
        self.drag_handle.setStyleSheet(self.global_styles)
        self.graph = TelemetryGraph()
        self.graph.setStyleSheet(self.global_styles)
        layout.addWidget(self.drag_handle)
        layout.addWidget(self.graph)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.setGeometry(100, 100, 300, 100)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_position:
            self.move((event.globalPosition() - self.drag_position).toPoint())
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName(APP_NAME)
    app.setApplicationName(APP_NAME)
    overlay = Overlay()
    overlay.setWindowTitle(APP_NAME)
    overlay.show()
    sys.exit(app.exec())
