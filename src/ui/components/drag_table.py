from PyQt6.QtWidgets import QTableWidget, QCheckBox, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal


class CheckBoxWidget(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 0px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
                border: 2px solid rgba(148, 163, 184, 0.4);
                background: rgba(15, 23, 42, 0.8);
            }
            QCheckBox::indicator:hover {
                border-color: rgba(59, 130, 246, 0.7);
                background: rgba(30, 41, 59, 0.9);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0
                border-color: transparent;
            }
            QCheckBox::indicator:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0
            }
        """)
        self.checkbox.toggled.connect(self.toggled.emit)
        layout.addWidget(self.checkbox)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, checked):
        self.checkbox.setChecked(checked)


class DragSelectTableBase(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
