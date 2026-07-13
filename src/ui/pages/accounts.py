from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTableWidgetItem, QInputDialog, QMessageBox, QMenu)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QAction
from src.ui.components.stats_bar import StatsBar
from src.ui.components.accounts_table import create_accounts_table
from src.ui.styles import BUTTON_PRIMARY, BUTTON_SECONDARY, BUTTON_DANGER, MESSAGE_BOX_STYLE, INPUT_DIALOG_STYLE
from src.ui.dialogs.styled_dialogs import show_info, show_warning, show_error, show_question, get_text
from src.core.database import Database
from src.core.cookie_manager import CookieManager
from src.ui.dialogs.add_account import AddAccountDialog


class AccountsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.cookie_manager = CookieManager()
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

        btn_add = self._make_button("Добавить аккаунт", primary=True)
        btn_add.clicked.connect(self._add_account)

        btn_set_tag = self._make_button("Установить тег")
        btn_set_tag.clicked.connect(self._set_tag)

        controls_layout.addWidget(btn_add)
        controls_layout.addWidget(btn_set_tag)
        controls_layout.addStretch()

        main_layout.addLayout(controls_layout)

        self.table = create_accounts_table()
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
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
            accounts = self.db.get_accounts()

            for row_idx, account in enumerate(accounts):
                self.table.insertRow(row_idx)

                id_item = QTableWidgetItem(str(account[0]))
                id_item.setForeground(Qt.GlobalColor.white)
                id_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(row_idx, 0, id_item)

                username_item = QTableWidgetItem(account[1] or "")
                username_item.setForeground(Qt.GlobalColor.white)
                username_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(row_idx, 1, username_item)

                proxy_text = f"{account[8]}:{account[9]}" if account[8] and account[9] else "---"
                proxy_item = QTableWidgetItem(proxy_text)
                proxy_item.setForeground(Qt.GlobalColor.white)
                proxy_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(row_idx, 2, proxy_item)

                tag_item = QTableWidgetItem(account[4] or "---")
                tag_item.setForeground(Qt.GlobalColor.white)
                tag_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(row_idx, 3, tag_item)

                videos_item = QTableWidgetItem(str(account[6] if len(account) > 6 else 0))
                videos_item.setForeground(Qt.GlobalColor.white)
                videos_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(row_idx, 4, videos_item)

            self._update_stats()
        except Exception as e:
            print(f"Ошибка загрузки аккаунтов: {e}")
            import traceback
            traceback.print_exc()

    def _update_stats(self):
        account_count = self.db.get_account_count()
        video_count = self.db.get_video_count()

        self.stats_bar.update_card_count("Аккаунты", account_count)
        self.stats_bar.update_card_count("Видео", video_count)

    def _add_account(self):
        dialog = AddAccountDialog(self)

        if dialog.exec() == AddAccountDialog.DialogCode.Accepted:
            mode, username, tag = dialog.get_result()
            self._login_account(username, tag)

    def _login_account(self, username, tag="default"):
        try:
            import pickle
            import time
            from pathlib import Path
            import undetected_chromedriver as uc
            import subprocess

            parent_path = Path(__file__).parent.parent.parent.parent

            QMessageBox.information(
                self,
                "Вход в TikTok",
                f"Сейчас откроется браузер.\n\nВойдите в TikTok для аккаунта: {username}\n\nБраузер закроется автоматически после входа."
            )

            def get_chrome_version():
                for binary in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
                    try:
                        out = subprocess.check_output([binary, "--version"], stderr=subprocess.DEVNULL).decode()
                        return int(out.strip().split()[-1].split(".")[0])
                    except (FileNotFoundError, ValueError, IndexError):
                        continue
                return 0

            options = uc.ChromeOptions()
            chrome_version = get_chrome_version()

            if chrome_version > 0:
                driver = uc.Chrome(options=options, version_main=chrome_version)
            else:
                driver = uc.Chrome(options=options)

            driver.get("https://www.tiktok.com/login")

            collected = {}
            timeout = 300
            start = time.time()

            while True:
                if time.time() - start > timeout:
                    driver.quit()
                    raise TimeoutError("Превышено время ожидания")

                try:
                    cookies = driver.get_cookies()
                    for cookie in cookies:
                        if cookie["name"] in ("sessionid", "tt-target-idc"):
                            collected[cookie["name"]] = cookie

                    if "sessionid" in collected and "tt-target-idc" in collected:
                        break
                except:
                    driver.quit()
                    raise Exception("Браузер закрыт")

                time.sleep(1)

            session_cookies = [collected["sessionid"], collected["tt-target-idc"]]

            driver.quit()

            cookies_dir = parent_path / "CookiesDir"
            cookies_dir.mkdir(exist_ok=True)
            cookie_file = cookies_dir / f"tiktok_session-{username}.cookie"

            with open(cookie_file, "wb") as f:
                pickle.dump(session_cookies, f)

            cookies_file = f"tiktok_session-{username}.cookie"
            self.db.save_account(username, cookies_file, tag=tag)
            self.load_data()

            show_info(self, "Успех", f"Аккаунт {username} добавлен с тегом '{tag}'!")

        except Exception as e:
            error_msg = str(e).lower()

            if "браузер закрыт" in error_msg or "closed" in error_msg:
                show_warning(self, "Действие отменено", "Вход отменён - браузер был закрыт.")
            else:
                show_error(self, "Ошибка", f"Ошибка входа:\n{str(e)}")


    def _show_context_menu(self, position: QPoint):
        row = self.table.rowAt(position.y())
        if row < 0:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                color:
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: rgba(59, 130, 246, 0.2);
            }
        """)

        edit_tag_action = QAction("🏷️ Изменить тег", self)
        edit_tag_action.triggered.connect(lambda: self._edit_tag_for_row(row))
        menu.addAction(edit_tag_action)

        menu.addSeparator()

        delete_action = QAction("🗑️ Удалить", self)
        delete_action.triggered.connect(lambda: self._delete_row(row))
        menu.addAction(delete_action)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def _edit_tag_for_row(self, row):
        """Изменить тег для конкретной строки"""
        account_id = int(self.table.item(row, 0).text())
        username = self.table.item(row, 1).text()
        current_tag = self.table.item(row, 3).text()
        if current_tag == "---":
            current_tag = ""

        existing_tags = self.db.get_account_tags()

        new_tag, ok = get_text(self, f"Изменить тег для '{username}'", f"Введите новый тег:\n\nСуществующие теги: {', '.join(existing_tags) if existing_tags else 'нет'}",
            text=current_tag
        )

        if ok and new_tag.strip():
            new_tag = new_tag.strip()
            updated = self.db.update_account_tags([account_id], new_tag)

            if updated > 0:
                self.load_data()
            else:
                show_warning(self, "Ошибка", "Не удалось обновить тег")

    def _delete_row(self, row):
        account_id = int(self.table.item(row, 0).text())
        username = self.table.item(row, 1).text()

        reply = show_question(
            self,
            "Подтверждение",
            f"Удалить аккаунт '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_accounts([account_id])
            self.cookie_manager.delete_cookies(username)
            self.load_data()

    def _set_tag(self):
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            show_warning(self, "Предупреждение", "Выберите хотя бы один аккаунт!")
            return

        existing_tags = self.db.get_account_tags()

        tag, ok = get_text(self, "Установить тег", f"Введите тег для {len(selected_rows)} аккаунт(ов):\n\nСуществующие теги: {', '.join(existing_tags) if existing_tags else 'нет'}",
            text=""
        )

        if ok and tag.strip():
            tag = tag.strip()
            account_ids = []

            for row in selected_rows:
                account_id = int(self.table.item(row, 0).text())
                account_ids.append(account_id)

            updated = self.db.update_account_tags(account_ids, tag)

            if updated > 0:
                self.load_data()
                show_info(self, "Успех", f"Тег '{tag}' установлен для {updated} аккаунт(ов)!")
            else:
                show_warning(self, "Ошибка", "Не удалось обновить теги")

    def _on_item_double_clicked(self, item):
        """Обработчик двойного клика на ячейку таблицы"""
        row = item.row()
        col = item.column()

        if col == 3:
            account_id = int(self.table.item(row, 0).text())
            current_tag = self.table.item(row, 3).text()
            if current_tag == "---":
                current_tag = ""

            existing_tags = self.db.get_account_tags()

            new_tag, ok = get_text(self, "Изменить тег", f"Введите новый тег:\n\nСуществующие теги: {', '.join(existing_tags) if existing_tags else 'нет'}",
                text=current_tag
            )

            if ok and new_tag.strip():
                new_tag = new_tag.strip()
                updated = self.db.update_account_tags([account_id], new_tag)

                if updated > 0:
                    self.load_data()
                    show_info(self, "Успех", f"Тег изменен на '{new_tag}'!")
                else:
                    show_warning(self, "Ошибка", "Не удалось обновить тег")
