
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)
from PySide6.QtCore import Signal, Qt

from assistant.chat_history import ChatHistory


class HistoryPanel(QWidget):

    conversation_selected = Signal(str)
    conversation_deleted = Signal(str)

    def __init__(self, history=None):
        super().__init__()

        self.history = history or ChatHistory()

        self.setWindowTitle("AI Assistant - Chat History")
        self.resize(420, 550)

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QListWidget {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 10px;
                padding: 8px;
            }

            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
            }

            QListWidget::item:selected {
                background-color: #2563eb;
            }

            QPushButton {
                background-color: #3b82f6;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("Chat History")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 10px;"
        )

        self.history_list = QListWidget()

        button_layout = QHBoxLayout()

        open_button = QPushButton("Open Chat")
        delete_button = QPushButton("Delete")

        button_layout.addWidget(open_button)
        button_layout.addWidget(delete_button)

        layout.addWidget(title)
        layout.addWidget(self.history_list)
        layout.addLayout(button_layout)

        open_button.clicked.connect(self.open_chat)
        delete_button.clicked.connect(self.delete_chat)

        self.history_list.itemDoubleClicked.connect(
            lambda item: self.open_chat()
        )

        self.refresh_history()

    def refresh_history(self):

        self.history_list.clear()

        conversations = self.history.get_all_conversations()

        for chat_id, chat in reversed(list(conversations.items())):

            title = chat.get("title", "New Conversation")

            item = QListWidgetItem(title)
            item.setData(Qt.ItemDataRole.UserRole, chat_id)

            self.history_list.addItem(item)

    def open_chat(self):

        item = self.history_list.currentItem()

        if item is None:
            return

        chat_id = item.data(Qt.ItemDataRole.UserRole)

        if self.history.open_chat(chat_id):
            self.conversation_selected.emit(chat_id)

    def delete_chat(self):

        item = self.history_list.currentItem()

        if item is None:
            return

        chat_id = item.data(Qt.ItemDataRole.UserRole)

        confirm = QMessageBox.question(
            self,
            "Delete Conversation",
            "Are you sure you want to delete this conversation?"
        )

        if confirm != QMessageBox.StandardButton.Yes:
            return

        if self.history.delete_chat(chat_id):
            self.conversation_deleted.emit(chat_id)
            self.refresh_history()