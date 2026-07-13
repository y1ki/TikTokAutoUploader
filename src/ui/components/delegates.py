from PyQt6.QtWidgets import QStyledItemDelegate, QCheckBox, QStyleOptionButton, QStyle, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint


class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        checked = index.data(Qt.ItemDataRole.UserRole)

        checkbox_style = QStyleOptionButton()
        checkbox_rect = self.get_checkbox_rect(option.rect)
        checkbox_style.rect = checkbox_rect
        checkbox_style.state = QStyle.StateFlag.State_Enabled

        if checked:
            checkbox_style.state |= QStyle.StateFlag.State_On
        else:
            checkbox_style.state |= QStyle.StateFlag.State_Off

        QApplication.style().drawControl(QStyle.ControlElement.CE_CheckBox, checkbox_style, painter)

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:
            checkbox_rect = self.get_checkbox_rect(option.rect)
            if checkbox_rect.contains(event.pos()):
                current = index.data(Qt.ItemDataRole.UserRole)
                model.setData(index, not current, Qt.ItemDataRole.UserRole)
                return True
        return False

    def get_checkbox_rect(self, rect):
        checkbox_rect = QRect(rect)
        checkbox_rect.setWidth(20)
        checkbox_rect.setHeight(20)
        checkbox_rect.moveCenter(rect.center())
        return checkbox_rect
