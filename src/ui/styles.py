DARK_THEME = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #0a0e27, stop:1 #16213e);
}

QWidget#content {
    background: transparent;
}

QLabel {
    color: #e4e4e7;
}
"""

SIDEBAR_STYLE = """
QWidget#sidebar {
    background: transparent;
}

QWidget#sidebar_container {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(30, 41, 59, 0.95),
                                stop:1 rgba(15, 23, 42, 0.95));
    border-radius: 20px;
    border: 1px solid rgba(148, 163, 184, 0.1);
}

QWidget#sidebar QPushButton {
    background-color: transparent;
    border: none;
    padding: 0px;
    margin: 0px;
    border-radius: 10px;
    color: #94a3b8;
}

QWidget#sidebar QPushButton:hover {
    background-color: rgba(59, 130, 246, 0.1);
    color: #60a5fa;
}

QWidget#sidebar QPushButton:pressed {
    background-color: rgba(59, 130, 246, 0.2);
}

QWidget#sidebar QPushButton[active="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgba(59, 130, 246, 0.8),
                                stop:1 rgba(37, 99, 235, 0.8));
    color: #ffffff;
    font-weight: bold;
}

QWidget#sidebar QPushButton[active="true"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgba(59, 130, 246, 0.9),
                                stop:1 rgba(37, 99, 235, 0.9));
}
"""

BUTTON_PRIMARY = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3b82f6, stop:1 #2563eb);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 0 24px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #2563eb, stop:1 #1d4ed8);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #1e40af, stop:1 #1e3a8a);
}
QPushButton:disabled {
    background: rgba(71, 85, 105, 0.5);
    color: rgba(203, 213, 225, 0.5);
}
"""

BUTTON_DANGER = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #ef4444, stop:1 #dc2626);
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 0 24px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #dc2626, stop:1 #b91c1c);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #b91c1c, stop:1 #991b1b);
}
"""

BUTTON_SECONDARY = """
QPushButton {
    background: rgba(30, 41, 59, 0.6);
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
    padding: 0 20px;
    font-weight: 500;
    font-size: 13px;
}
QPushButton:hover {
    background: rgba(51, 65, 85, 0.8);
    color: #f1f5f9;
    border-color: rgba(148, 163, 184, 0.3);
}
QPushButton:pressed {
    background: rgba(71, 85, 105, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
}
QPushButton:disabled {
    background: rgba(30, 41, 59, 0.3);
    color: rgba(203, 213, 225, 0.3);
}
"""

PROGRESS_BAR = """
QProgressBar {
    background-color: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 8px;
    text-align: center;
    color: #e4e4e7;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3b82f6, stop:1 #8b5cf6);
    border-radius: 7px;
}
"""

TABLE_STYLE = """
QTableWidget {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 16px;
    gridline-color: transparent;
    color: #e4e4e7;
}
QTableWidget::item {
    padding: 12px 16px;
    border: none;
    border-bottom: 1px solid rgba(148, 163, 184, 0.05);
}
QTableWidget::item:hover {
    background-color: rgba(59, 130, 246, 0.1);
}
QTableWidget::item:selected {
    background-color: rgba(59, 130, 246, 0.2);
}
QHeaderView::section {
    background: rgba(30, 41, 59, 0.8);
    color: #94a3b8;
    padding: 12px 16px;
    border: none;
    border-bottom: 2px solid rgba(59, 130, 246, 0.3);
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QHeaderView::section:hover {
    background: rgba(51, 65, 85, 0.9);
    color: #cbd5e1;
}
QScrollBar:vertical {
    background-color: transparent;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgba(59, 130, 246, 0.3),
                                stop:1 rgba(139, 92, 246, 0.3));
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgba(59, 130, 246, 0.5),
                                stop:1 rgba(139, 92, 246, 0.5));
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
QScrollBar:horizontal {
    background-color: transparent;
    height: 10px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(59, 130, 246, 0.3),
                                stop:1 rgba(139, 92, 246, 0.3));
    border-radius: 5px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(59, 130, 246, 0.5),
                                stop:1 rgba(139, 92, 246, 0.5));
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}
"""

MESSAGE_BOX_STYLE = """
QMessageBox {
    background-color: #ffffff;
}
QMessageBox QLabel {
    color: #1e293b;
    font-size: 13px;
}
QMessageBox QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3b82f6, stop:1 #2563eb);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #2563eb, stop:1 #1d4ed8);
}
"""

INPUT_DIALOG_STYLE = """
QInputDialog {
    background-color: #ffffff;
}
QInputDialog QLabel {
    color: #1e293b;
    font-size: 13px;
}
QInputDialog QLineEdit {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    color: #1e293b;
    font-size: 13px;
}
QInputDialog QLineEdit:focus {
    border-color: #3b82f6;
}
QInputDialog QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3b82f6, stop:1 #2563eb);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-width: 80px;
}
QInputDialog QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #2563eb, stop:1 #1d4ed8);
}
"""

PROGRESS_DIALOG_STYLE = """
QProgressDialog {
    background-color: #ffffff;
}
QProgressDialog QLabel {
    color: #1e293b;
    font-size: 13px;
}
QProgressDialog QPushButton {
    background: rgba(239, 68, 68, 0.9);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-width: 80px;
}
QProgressDialog QPushButton:hover {
    background: rgba(220, 38, 38, 1);
}
QProgressDialog QProgressBar {
    background-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    text-align: center;
    color: #1e293b;
    height: 20px;
}
QProgressDialog QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3b82f6, stop:1 #8b5cf6);
    border-radius: 5px;
}
"""
