
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)

from assistant.chat_history import ChatHistory
from assistant.ui.history_panel import HistoryPanel
from assistant.ui.workers import AIWorker


class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Assistant")
        self.resize(420, 600)

        self.history = ChatHistory()
        self.history_panel = None
        self.worker = None

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-size: 14px;
            }

            QTextEdit {
                background-color: #1f2937;
                border: 1px solid #374151;
                border-radius: 10px;
                padding: 10px;
            }

            QLineEdit {
                background-color: #1f2937;
                border: 1px solid #4f8cff;
                border-radius: 10px;
                padding: 12px;
            }

            QPushButton {
                background-color: #4f8cff;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("AI Assistant")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; padding: 10px;"
        )

        top_layout = QHBoxLayout()

        self.new_chat_button = QPushButton("New Chat")
        self.history_button = QPushButton("History")

        top_layout.addWidget(self.new_chat_button)
        top_layout.addWidget(self.history_button)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")

        self.send_button = QPushButton("Send")

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input_box)
        bottom_layout.addWidget(self.send_button)

        layout.addWidget(title)
        layout.addLayout(top_layout)
        layout.addWidget(self.chat_area)
        layout.addLayout(bottom_layout)

        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        self.new_chat_button.clicked.connect(self.new_chat)
        self.history_button.clicked.connect(self.show_history)

        self.load_current_chat()

    def load_current_chat(self):

        self.chat_area.clear()

        for item in self.history.get_messages():
            role = "You" if item["role"] == "user" else "AI"

            self.chat_area.append(
                role + ": " + item["content"]
            )

    def new_chat(self):

        if self.worker and self.worker.isRunning():
            return

        self.history.new_chat()

        self.chat_area.clear()
        self.input_box.clear()

    def show_history(self):

        if self.history_panel is None:

            self.history_panel = HistoryPanel(self.history)

            self.history_panel.conversation_selected.connect(
                self.open_conversation
            )

            self.history_panel.conversation_deleted.connect(
                self.on_conversation_deleted
            )

        self.history_panel.refresh_history()
        self.history_panel.show()
        self.history_panel.activateWindow()
        self.history_panel.raise_()

    def open_conversation(self, chat_id):

        if self.worker and self.worker.isRunning():
            return

        if self.history.open_chat(chat_id):

            self.load_current_chat()

            self.show()
            self.activateWindow()
            self.raise_()

    def on_conversation_deleted(self, chat_id):

        if self.history.current_chat_id is None:
            self.chat_area.clear()

    def send_message(self):

        message = self.input_box.text().strip()

        if not message:
            return

        if self.worker and self.worker.isRunning():
            return

        self.chat_area.append("You: " + message)

        self.history.add_message("user", message)

        self.input_box.clear()

        self.send_button.setEnabled(False)

        self.chat_area.append("AI: Thinking...")

        self.worker = AIWorker(message)

        self.worker.finished_response.connect(
            self.show_response
        )

        self.worker.error_occurred.connect(
            self.show_error
        )

        self.worker.start()

    def show_response(self, response):

        self.replace_thinking(response)

        self.history.add_message("assistant", response)

        self.send_button.setEnabled(True)

        if self.history_panel is not None:
            self.history_panel.refresh_history()

    def show_error(self, error):

        self.replace_thinking("Error: " + error)

        self.history.add_message(
            "assistant",
            "Error: " + error
        )

        self.send_button.setEnabled(True)

    def replace_thinking(self, response):

        cursor = self.chat_area.textCursor()

        cursor.movePosition(cursor.MoveOperation.End)

        cursor.select(
            cursor.SelectionType.BlockUnderCursor
        )

        cursor.removeSelectedText()

        cursor.insertText("AI: " + response)

        self.chat_area.append("")

    def apply_theme(self, theme):

        if theme == "Light":

            self.setStyleSheet("""
                QWidget {
                    background-color: #f3f4f6;
                    color: #111827;
                }

                QTextEdit, QLineEdit {
                    background-color: white;
                    color: #111827;
                    border: 1px solid #9ca3af;
                    border-radius: 10px;
                    padding: 10px;
                }

                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                }
            """)

        else:

            self.setStyleSheet("""
                QWidget {
                    background-color: #111827;
                    color: white;
                }

                QTextEdit, QLineEdit {
                    background-color: #1f2937;
                    color: white;
                    border: 1px solid #374151;
                    border-radius: 10px;
                    padding: 10px;
                }

                QPushButton {
                    background-color: #4f8cff;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                }
            """)