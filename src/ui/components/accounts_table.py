from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt
from src.ui.components.drag_table import DragSelectTableBase
from src.ui.styles import TABLE_STYLE


def create_accounts_table():
    table = DragSelectTableBase()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID", "Username", "Прокси", "Тег", "Видео"])

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    table.verticalHeader().setVisible(False)
    table.verticalHeader().setDefaultSectionSize(56)
    table.setSelectionBehavior(DragSelectTableBase.SelectionBehavior.SelectRows)
    table.setSelectionMode(DragSelectTableBase.SelectionMode.MultiSelection)
    table.setShowGrid(False)
    table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    table.setStyleSheet(TABLE_STYLE)

    return table
