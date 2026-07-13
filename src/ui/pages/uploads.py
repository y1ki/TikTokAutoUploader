from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QFileDialog, QTextEdit, QLineEdit, QComboBox, QMessageBox, QProgressDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from src.ui.components.stats_bar import StatsBar
from src.ui.styles import BUTTON_PRIMARY, BUTTON_SECONDARY, MESSAGE_BOX_STYLE, PROGRESS_DIALOG_STYLE
from src.ui.dialogs.styled_dialogs import show_info, show_warning, show_error
from src.core.database import Database


class UploadThread(QThread):
    """Поток для загрузки видео в фоне"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, int)
    error = pyqtSignal(str)

    def __init__(self, video_path, title, tag, accounts, db):
        super().__init__()
        self.video_path = video_path
        self.title = title
        self.tag = tag
        self.accounts = accounts
        self.db = db

    def run(self):
        try:
            import os
            if not os.path.exists(self.video_path):
                self.error.emit("Видео файл не найден!")
                return

            from tiktok_uploader import tiktok

            uploaded_count = 0
            total = len(self.accounts)

            for idx, account in enumerate(self.accounts, 1):
                username = account[0]

                self.progress.emit(f"Загрузка на аккаунт {username} ({idx}/{total})...")

                try:
                    tiktok.upload_video(
                        session_user=username,
                        video=self.video_path,
                        title=self.title,
                        schedule_time=0,
                        allow_comment=1,
                        allow_duet=0,
                        allow_stitch=0,
                        visibility_type=0,
                        brand_organic_type=0,
                        branded_content_type=0,
                        ai_label=0,
                        proxy=None
                    )
                    uploaded_count += 1
                    self.progress.emit(f"✓ Загружено на {username} ({uploaded_count}/{total})")
                except Exception as e:
                    self.progress.emit(f"✗ Ошибка на {username}: {str(e)}")
                    continue

            self.finished.emit(uploaded_count, total)

        except Exception as e:
            self.error.emit(f"Критическая ошибка: {str(e)}")


class UploadsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.selected_video = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        self.stats_bar = StatsBar()
        main_layout.addWidget(self.stats_bar)
        self._update_stats()

        upload_container = QWidget()
        upload_container.setStyleSheet("""
            QWidget {
                background-color: rgba(25, 25, 28, 0.8);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        upload_layout = QVBoxLayout(upload_container)
        upload_layout.setContentsMargins(24, 24, 24, 24)
        upload_layout.setSpacing(16)

        title_label = QLabel("Загрузка видео")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #94a3b8;")
        upload_layout.addWidget(title_label)

        video_layout = QHBoxLayout()
        video_layout.setSpacing(12)

        self.video_label = QLabel("Видео не выбрано")
        self.video_label.setFont(QFont("Segoe UI", 10))
        self.video_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); background: transparent; border: none;")

        btn_select_video = self._make_button("Выбрать видео", primary=True)
        btn_select_video.clicked.connect(self._select_video)

        video_layout.addWidget(self.video_label, 1)
        video_layout.addWidget(btn_select_video)
        upload_layout.addLayout(video_layout)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)

        title_form_label = QLabel("Название:")
        title_form_label.setFont(QFont("Segoe UI", 10))
        title_form_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent; border: none;")
        form_layout.addWidget(title_form_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите название видео")
        self.title_input.setFixedHeight(40)
        self.title_input.setFont(QFont("Segoe UI", 10))
        self.title_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(15, 15, 17, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 0 12px;
                color:
            }
            QLineEdit:focus {
                border-color: rgba(59, 130, 246, 0.5);
            }
        """)
        form_layout.addWidget(self.title_input)

        desc_form_label = QLabel("Описание:")
        desc_form_label.setFont(QFont("Segoe UI", 10))
        desc_form_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent; border: none;")
        form_layout.addWidget(desc_form_label)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Введите описание видео")
        self.description_input.setFixedHeight(100)
        self.description_input.setFont(QFont("Segoe UI", 10))
        self.description_input.setStyleSheet("""
            QTextEdit {
                background-color: rgba(15, 15, 17, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px;
                color:
            }
            QTextEdit:focus {
                border-color: rgba(59, 130, 246, 0.5);
            }
        """)
        form_layout.addWidget(self.description_input)

        account_form_label = QLabel("Тег аккаунтов:")
        account_form_label.setFont(QFont("Segoe UI", 10))
        account_form_label.setStyleSheet("color: #94a3b8;")
        form_layout.addWidget(account_form_label)

        self.account_combo = QComboBox()
        self.account_combo.setFixedHeight(40)
        self.account_combo.setFont(QFont("Segoe UI", 10))
        self.account_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(30, 41, 59, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 0 12px;
                color:
            }
            QComboBox:focus {
                border-color: rgba(59, 130, 246, 0.5);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.2);
                selection-background-color: rgba(59, 130, 246, 0.3);
                color:
            }
        """)
        self._load_tags()
        form_layout.addWidget(self.account_combo)

        upload_layout.addLayout(form_layout)

        btn_upload = self._make_button("Загрузить видео", primary=True)
        btn_upload.clicked.connect(self._upload_video)
        btn_upload.setFixedWidth(200)
        upload_layout.addWidget(btn_upload, 0, Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(upload_container)
        main_layout.addStretch()

    def _make_button(self, text: str, primary: bool = False) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedHeight(40)
        btn.setMinimumWidth(140)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold if primary else QFont.Weight.Normal))
        btn.setStyleSheet(BUTTON_PRIMARY if primary else BUTTON_SECONDARY)
        return btn

    def _update_stats(self):
        account_count = self.db.get_account_count()
        proxy_count = self.db.get_proxy_count()
        video_count = self.db.get_video_count()

        self.stats_bar.update_card_count("Аккаунты", account_count)
        self.stats_bar.update_card_count("Прокси", proxy_count)
        self.stats_bar.update_card_count("Видео", video_count)

    def _load_tags(self):
        self.account_combo.clear()
        tags = self.db.get_account_tags()
        for tag in tags:
            self.account_combo.addItem(f"Тег: {tag}", tag)

    def _select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать видео",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)"
        )

        if file_path:
            self.selected_video = file_path
            import os
            filename = os.path.basename(file_path)
            self.video_label.setText(f"Выбрано: {filename}")
            self.video_label.setStyleSheet("color: rgba(59, 130, 246, 0.9); background: transparent; border: none;")

    def _upload_video(self):
        if not self.selected_video:
            self.video_label.setText("Сначала выберите видео!")
            self.video_label.setStyleSheet("color: #94a3b8;")
            return

        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        tag = self.account_combo.currentData()

        if not title:
            title = "Untitled"

        if not tag:
            show_warning(self, "Ошибка", "Выберите тег для загрузки!")
            return

        try:
            video_id = self.db.save_video(self.selected_video, title, description)
            self._start_upload_to_tiktok(tag, video_id, title, description)
        except Exception as e:
            show_error(self, "Ошибка", f"Ошибка:\n{str(e)}")

    def _start_upload_to_tiktok(self, tag, video_id, title, description):
        try:
            import sys
            from pathlib import Path

            parent_path = Path(__file__).parent.parent.parent.parent
            sys.path.insert(0, str(parent_path))

            accounts = self.db.fetchall("SELECT username FROM accounts WHERE tag = ? AND status = 'active'", (tag,))

            if not accounts:
                show_error(self, "Ошибка", f"Нет аккаунтов с тегом '{tag}'!")
                return

            self.progress_dialog = QProgressDialog("Подготовка к загрузке...", "Отмена", 0, 0, self)
            self.progress_dialog.setStyleSheet(PROGRESS_DIALOG_STYLE)
            self.progress_dialog.setWindowTitle("Загрузка видео")
            self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setFixedSize(450, 150)
            self.progress_dialog.canceled.connect(self._cancel_upload)

            self.upload_thread = UploadThread(self.selected_video, title, tag, accounts, self.db)
            self.upload_thread.progress.connect(self._on_upload_progress)
            self.upload_thread.finished.connect(self._on_upload_finished)
            self.upload_thread.error.connect(self._on_upload_error)
            self.upload_thread.start()

        except Exception as e:
            show_error(self, "Ошибка", f"Ошибка загрузки:\n{str(e)}")

    def _on_upload_progress(self, message):
        """Обновление прогресса загрузки"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.setLabelText(message)

    def _on_upload_finished(self, uploaded_count, total):
        """Завершение загрузки"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()

        self.selected_video = None
        self.video_label.setText(f"✓ Загружено на {uploaded_count} из {total} аккаунтов")
        self.video_label.setStyleSheet("color: #94a3b8;")
        self.title_input.clear()
        self.description_input.clear()
        self._update_stats()

        msg = QMessageBox(self)
        msg.setStyleSheet(MESSAGE_BOX_STYLE)
        if uploaded_count > 0:
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Успех")
            msg.setText(f"Видео успешно загружено на {uploaded_count} из {total} аккаунтов!")
        else:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Предупреждение")
            msg.setText("Не удалось загрузить видео ни на один аккаунт")
        msg.exec()

    def _on_upload_error(self, error_message):
        """Обработка ошибки загрузки"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()

        msg = QMessageBox(self)
        msg.setStyleSheet(MESSAGE_BOX_STYLE)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(error_message)
        msg.exec()

    def _cancel_upload(self):
        """Отмена загрузки"""
        if hasattr(self, 'upload_thread') and self.upload_thread.isRunning():
            self.upload_thread.terminate()
            self.upload_thread.wait()
            msg = QMessageBox(self)
            msg.setStyleSheet(MESSAGE_BOX_STYLE)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Отменено")
            msg.setText("Загрузка отменена пользователем")
            msg.exec()
