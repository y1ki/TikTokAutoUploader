from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QLineEdit, QFileDialog, QRadioButton, QButtonGroup, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.ui.styles import BUTTON_PRIMARY, BUTTON_SECONDARY


class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить аккаунт")
        self.setFixedSize(450, 320)
        self.setStyleSheet("""
            QDialog {
                background-color:
            }
            QLabel {
                color:
            }
            QRadioButton {
                color:
                font-size: 11px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
        """)

        self.mode = None
        self.username = None
        self.tag = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Добавить новый аккаунт")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        desc = QLabel("Откроется браузер для входа в TikTok.\nПосле входа куки автоматически сохранятся.")
        desc.setFont(QFont("Segoe UI", 10))
        desc.setStyleSheet("color: #94a3b8;")
        layout.addWidget(desc)

        username_label = QLabel("Имя аккаунта:")
        username_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя для аккаунта")
        self.username_input.setFixedHeight(40)
        self.username_input.setFont(QFont("Segoe UI", 10))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 0 12px;
                color:
            }
            QLineEdit:focus {
                border-color: rgba(59, 130, 246, 0.5);
            }
        """)
        layout.addWidget(self.username_input)

        tag_label = QLabel("Тег группы:")
        tag_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(tag_label)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Введите тег для группировки")
        self.tag_input.setFixedHeight(40)
        self.tag_input.setFont(QFont("Segoe UI", 10))
        self.tag_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 0 12px;
                color:
            }
            QLineEdit:focus {
                border-color: rgba(59, 130, 246, 0.5);
            }
        """)
        layout.addWidget(self.tag_input)

        layout.addStretch()

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setFixedHeight(40)
        btn_cancel.setMinimumWidth(120)
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setFont(QFont("Segoe UI", 9))
        btn_cancel.setStyleSheet(BUTTON_SECONDARY)
        btn_cancel.clicked.connect(self.reject)

        btn_ok = QPushButton("Продолжить")
        btn_ok.setFixedHeight(40)
        btn_ok.setMinimumWidth(120)
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        btn_ok.setStyleSheet(BUTTON_PRIMARY)
        btn_ok.clicked.connect(self.accept_action)

        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_cancel)
        buttons_layout.addWidget(btn_ok)

        layout.addLayout(buttons_layout)

    def accept_action(self):
        username = self.username_input.text().strip()
        tag = self.tag_input.text().strip()

        if not username:
            QMessageBox.warning(self, "Ошибка", "Введите имя аккаунта!")
            return

        if not tag:
            QMessageBox.warning(self, "Ошибка", "Введите тег!")
            return

        self.username = username
        self.tag = tag
        self.mode = "login"

        self.accept()

    def get_result(self):
        return self.mode, self.username, self.tag
