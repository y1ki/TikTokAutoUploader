from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from pathlib import Path
from src.ui.styles import DARK_THEME, SIDEBAR_STYLE
from src.ui.components.sidebar import Sidebar
from src.ui.pages.accounts import AccountsPage
from src.ui.pages.proxies import ProxiesPage
from src.ui.pages.uploads import UploadsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TikTok Auto Uploader")
        self.setFixedSize(1200, 700)
        self.setStyleSheet(DARK_THEME)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.on_page_changed)
        self.sidebar.setStyleSheet(SIDEBAR_STYLE)
        main_layout.addWidget(self.sidebar)

        content_container = QWidget()
        content_container.setObjectName("content")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()
        self.accounts_page = AccountsPage()
        self.proxies_page = ProxiesPage()
        self.uploads_page = UploadsPage()

        self.pages.addWidget(self.accounts_page)
        self.pages.addWidget(self.proxies_page)
        self.pages.addWidget(self.uploads_page)

        content_layout.addWidget(self.pages)
        main_layout.addWidget(content_container)

    def on_page_changed(self, index):
        self.pages.setCurrentIndex(index)
        if index == 0:
            self.accounts_page.load_data()
        elif index == 1:
            self.proxies_page.load_data()
