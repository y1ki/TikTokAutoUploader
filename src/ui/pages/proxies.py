from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidgetItem, QFileDialog, QInputDialog, QLabel)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from src.ui.components.stats_bar import StatsBar
from src.ui.components.proxy_table import create_proxy_table
from src.ui.components.drag_table import CheckBoxWidget
from src.ui.styles import BUTTON_PRIMARY, BUTTON_SECONDARY, BUTTON_DANGER
from src.core.database import Database


class ProxiesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        self.stats_bar = StatsBar()
        main_layout.addWidget(self.stats_bar)
        self._update_stats()

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(12)

        btn_load = self._make_button("Загрузить прокси", primary=True)
        btn_load.clicked.connect(self._load_proxies)

        btn_delete = self._make_button("Удалить выбранные")
        btn_delete.clicked.connect(self._delete_selected)

        btn_set_tag = self._make_button("Установить тег")
        btn_set_tag.clicked.connect(self._set_tag)

        controls_layout.addWidget(btn_load)
        controls_layout.addWidget(btn_delete)
        controls_layout.addWidget(btn_set_tag)
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        self.table = create_proxy_table()
        main_layout.addWidget(self.table)

    def _make_button(self, text: str, primary: bool = False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setMinimumWidth(140)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold if primary else QFont.Weight.Normal))
        btn.setStyleSheet(BUTTON_PRIMARY if primary else BUTTON_SECONDARY)
        return btn

    def load_data(self):
        try:
            self.table.setRowCount(0)
            proxies = self.db.load_proxies()

            for row_idx, proxy in enumerate(proxies):
                self.table.insertRow(row_idx)

                checkbox_widget = CheckBoxWidget()
                self.table.setCellWidget(row_idx, 0, checkbox_widget)

                self.table.setItem(row_idx, 1, QTableWidgetItem(proxy['ip']))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(proxy['port'])))

                ping_text = f"{proxy['response_time']:.0f}ms" if proxy['response_time'] else "---"
                self.table.setItem(row_idx, 3, QTableWidgetItem(ping_text))

                self.table.setItem(row_idx, 4, QTableWidgetItem(proxy['login'] or "---"))
                self.table.setItem(row_idx, 5, QTableWidgetItem(proxy['password'] or "---"))
                self.table.setItem(row_idx, 6, QTableWidgetItem(proxy['protocol'].upper()))
                self.table.setItem(row_idx, 7, QTableWidgetItem(proxy['status'].upper()))
                self.table.setItem(row_idx, 8, QTableWidgetItem(proxy['tag']))

                for col in range(1, 9):
                    item = self.table.item(row_idx, col)
                    if item:
                        item.setForeground(Qt.GlobalColor.white)
                        item.setFont(QFont("Segoe UI", 9))

                item = self.table.item(row_idx, 1)
                if item:
                    item.setData(Qt.ItemDataRole.UserRole, proxy['id'])

            self._update_stats()
        except Exception as e:
            print(f"Ошибка загрузки прокси: {e}")

    def _update_stats(self):
        account_count = self.db.get_account_count()
        proxy_count = self.db.get_proxy_count()
        video_count = self.db.get_video_count()

        self.stats_bar.update_card_count("Аккаунты", account_count)
        self.stats_bar.update_card_count("Прокси", proxy_count)
        self.stats_bar.update_card_count("Видео", video_count)

    def _load_proxies(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать файл с прокси",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        try:
            import sys
            from pathlib import Path
            parent_path = Path(__file__).parent.parent.parent.parent
            sys.path.insert(0, str(parent_path))

            from tiktok_uploader.proxy_checker import ProxyChecker
            loaded_proxies, duplicates = ProxyChecker.load_proxies_from_file(file_path)

            if loaded_proxies:
                saved, dups = self.db.save_proxies(loaded_proxies)
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки прокси:\n{str(e)}")

    def _delete_selected(self):
        selected_ids = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                item = self.table.item(row, 1)
                if item:
                    proxy_id = item.data(Qt.ItemDataRole.UserRole)
                    selected_ids.append(proxy_id)

        if selected_ids:
            self.db.delete_proxies(selected_ids)
            self.load_data()

    def _set_tag(self):
        selected_ids = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                item = self.table.item(row, 1)
                if item:
                    proxy_id = item.data(Qt.ItemDataRole.UserRole)
                    selected_ids.append(proxy_id)

        if not selected_ids:
            return

        tag, ok = QInputDialog.getText(self, "Установить тег", "Введите тег:")
        if ok and tag:
            self.db.update_proxy_tags(selected_ids, tag)
            self.load_data()
