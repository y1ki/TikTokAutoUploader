import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from src.ui.windows.main import MainWindow
from src.core.database import Database


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        self.db = Database()

    def run(self):
        QDesktopServices.openUrl(QUrl("https://t.me/Y1kiLOLZ"))
        self.show_main_window()
        return self.app.exec()

    def show_main_window(self):
        if self.main_window is None:
            self.main_window = MainWindow()
        self.main_window.show()
