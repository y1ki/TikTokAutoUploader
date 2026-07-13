from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from src.ui.components.delegates import CheckBoxDelegate
from src.ui.components.drag_table import DragSelectTableBase
from src.ui.styles import TABLE_STYLE


def create_proxy_table():
    table = DragSelectTableBase()
    table.setColumnCount(9)
    table.setHorizontalHeaderLabels(["", "IP", "PORT", "PING", "LOGIN", "PASSWORD", "ПРОТОКОЛ", "СТАТУС", "ТЕГ"])

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)

    table.setColumnWidth(0, 40)

    table.verticalHeader().setVisible(False)
    table.verticalHeader().setDefaultSectionSize(56)
    table.setSelectionMode(DragSelectTableBase.SelectionMode.NoSelection)
    table.setShowGrid(False)
    table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    table.setItemDelegateForColumn(0, CheckBoxDelegate(table))
    table.setStyleSheet(TABLE_STYLE)

    header.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    return table
