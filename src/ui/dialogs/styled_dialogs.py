"""Стилизованные диалоги для приложения"""
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from src.ui.styles import MESSAGE_BOX_STYLE, INPUT_DIALOG_STYLE


def show_message(parent, title, text, icon=QMessageBox.Icon.Information):
    """Показать стилизованное информационное сообщение"""
    msg = QMessageBox(parent)
    msg.setStyleSheet(MESSAGE_BOX_STYLE)
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(text)
    return msg.exec()


def show_info(parent, title, text):
    """Показать информационное сообщение"""
    return show_message(parent, title, text, QMessageBox.Icon.Information)


def show_warning(parent, title, text):
    """Показать предупреждение"""
    return show_message(parent, title, text, QMessageBox.Icon.Warning)


def show_error(parent, title, text):
    """Показать ошибку"""
    return show_message(parent, title, text, QMessageBox.Icon.Critical)


def show_question(parent, title, text):
    """Показать вопрос с кнопками Да/Нет"""
    msg = QMessageBox(parent)
    msg.setStyleSheet(MESSAGE_BOX_STYLE)
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return msg.exec()


def get_text(parent, title, label, text=""):
    """Получить текст от пользователя"""
    dialog = QInputDialog(parent)
    dialog.setStyleSheet(INPUT_DIALOG_STYLE)
    dialog.setWindowTitle(title)
    dialog.setLabelText(label)
    dialog.setTextValue(text)
    dialog.resize(400, 150)

    ok = dialog.exec()
    return dialog.textValue(), ok == QInputDialog.DialogCode.Accepted
