
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel,
    QScrollArea, QFrame
)

from assistant.ui.settings_window import SettingsWindow


class MessageBubble(QFrame):

    def __init__(self, text, is_user=True):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)

        if is_user:
            lbl.setStyleSheet("""
                background-color: #0078D4;
                color: white;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 13px;
            """)
            layout.addStretch()
            layout.addWidget(lbl)

        else:
            lbl.setStyleSheet("""
                background-color: #2D2D2D;
                color: #E0E0E0;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 13px;
            """)
            layout.addWidget(lbl)
            layout.addStretch()


class ChatWindow(QWidget):

    def __init__(self, hotkey_manager=None):
        super().__init__()

        self.setWindowTitle("AI Assistant")
        self.resize(380, 520)
        self.setStyleSheet("background-color: #1E1E1E;")

        # Settings Window
        self.settings_window = SettingsWindow(
            self, hotkey_manager
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header
        header_layout = QHBoxLayout()

        title_lbl = QLabel("AI Assistant")
        title_lbl.setStyleSheet(
            "color: white; font-weight: bold; font-size: 14px;"
        )

        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.settings_btn.clicked.connect(self.open_settings)

        self.clear_btn = QPushButton("🗑️ Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888888;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #FF5555;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_chat)

        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_btn)
        header_layout.addWidget(self.clear_btn)

        main_layout.addLayout(header_layout)

        # Chat Messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "border: none; background-color: transparent;"
        )

        self.container = QWidget()
        self.chat_layout = QVBoxLayout(self.container)
        self.chat_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

        # Typing Indicator
        self.typing_label = QLabel("AI is typing...")
        self.typing_label.setStyleSheet(
            "color: #888888; font-size: 11px; font-style: italic;"
        )
        self.typing_label.hide()

        main_layout.addWidget(self.typing_label)

        # Input Area
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                color: white;
                border: 1px solid #3C3C3C;
                border-radius: 6px;
                padding: 6px 10px;
            }
        """)

        self.input_field.returnPressed.connect(self.send_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        """)

        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)

        main_layout.addLayout(input_layout)

    def add_message(self, text, is_user=True):

        bubble = MessageBubble(text, is_user)
        self.chat_layout.addWidget(bubble)

        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def send_message(self):

        text = self.input_field.text().strip()

        if text:
            self.add_message(text, is_user=True)
            self.input_field.clear()
            self.show_typing(True)

    def show_typing(self, show=True):

        if show:
            self.typing_label.show()
        else:
            self.typing_label.hide()

    def clear_chat(self):

        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        self.show_typing(False)

    def open_settings(self):

        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()
