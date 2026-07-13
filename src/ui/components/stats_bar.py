from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor


class StatCard(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, title: str, count: int = 0, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_active = False
        self.setup_ui(count)

    def setup_ui(self, count: int):
        self.setFixedHeight(100)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(30, 41, 59, 0.6),
                                            stop:1 rgba(15, 23, 42, 0.6));
                border: 1px solid rgba(148, 163, 184, 0.15);
                border-radius: 20px;
            }
            QWidget:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(51, 65, 85, 0.8),
                                            stop:1 rgba(30, 41, 59, 0.8));
                border-color: rgba(59, 130, 246, 0.3);
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(0)

        left_container = QWidget()
        left_layout = QHBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(16)

        self.count_label = QLabel(str(count))
        self.count_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        self.count_label.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #60a5fa, stop:1 #a78bfa);
            background: transparent;
            border: none;
        """)

        title_label = QLabel(self.title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #94a3b8; background: transparent; border: none;")

        left_layout.addWidget(self.count_label)
        left_layout.addWidget(title_label, 1)

        layout.addWidget(left_container)

    def update_count(self, count: int):
        self.count_label.setText(str(count))

    def set_active(self, active: bool):
        self.is_active = active
        if active:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 rgba(59, 130, 246, 0.3),
                                                stop:1 rgba(139, 92, 246, 0.3));
                    border: 2px solid rgba(59, 130, 246, 0.5);
                    border-radius: 20px;
                }
                QWidget:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                stop:0 rgba(59, 130, 246, 0.4),
                                                stop:1 rgba(139, 92, 246, 0.4));
                    border-color: rgba(59, 130, 246, 0.7);
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 rgba(30, 41, 59, 0.6),
                                                stop:1 rgba(15, 23, 42, 0.6));
                    border: 1px solid rgba(148, 163, 184, 0.15);
                    border-radius: 20px;
                }
                QWidget:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                stop:0 rgba(51, 65, 85, 0.8),
                                                stop:1 rgba(30, 41, 59, 0.8));
                    border-color: rgba(59, 130, 246, 0.3);
                }
            """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.title)
        super().mousePressEvent(event)


class StatsBar(QWidget):
    card_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = {}
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        card_titles = ["Аккаунты", "Видео"]

        for title in card_titles:
            card = StatCard(title, 0)
            card.clicked.connect(self.card_clicked.emit)
            self.cards[title] = card
            layout.addWidget(card)

    def update_card_count(self, title: str, count: int):
        if title in self.cards:
            self.cards[title].update_count(count)

    def set_active_card(self, title: str):
        for card_title, card in self.cards.items():
            card.set_active(card_title == title)

    def clear_active(self):
        for card in self.cards.values():
            card.set_active(False)
