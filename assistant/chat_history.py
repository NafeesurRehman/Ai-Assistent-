import json
import uuid
from pathlib import Path
from datetime import datetime


class ChatHistory:

    def __init__(self):
        self.file = (
            Path(__file__).resolve().parent.parent
            / "conversations.json"
        )
        self.conversations = {}
        self.current_chat_id = None
        self.load()

    def load(self):
        if self.file.exists():
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    self.conversations = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.conversations = {}

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.conversations, f, indent=4, ensure_ascii=False)

    def new_chat(self):
        chat_id = str(uuid.uuid4())
        self.conversations[chat_id] = {
            "title": "New Conversation",
            "created": datetime.now().isoformat(),
            "messages": []
        }
        self.current_chat_id = chat_id
        self.save()
        return chat_id

    def add_message(self, role, content):
        if not self.current_chat_id:
            self.new_chat()

        chat = self.conversations[self.current_chat_id]
        chat["messages"].append({
            "role": role,
            "content": content
        })

        if len(chat["messages"]) == 1 and role == "user":
            chat["title"] = content[:40]

        self.save()

    def get_messages(self, chat_id=None):
        chat_id = chat_id or self.current_chat_id
        if not chat_id or chat_id not in self.conversations:
            return []
        return self.conversations[chat_id]["messages"]

    def get_all_conversations(self):
        return self.conversations

    def open_chat(self, chat_id):
        if chat_id not in self.conversations:
            return False
        self.current_chat_id = chat_id
        return True

    def delete_chat(self, chat_id):
        if chat_id not in self.conversations:
            return False

        del self.conversations[chat_id]

        if self.current_chat_id == chat_id:
            self.current_chat_id = None

        self.save()
        return True

    def clear(self):
        self.current_chat_id = None
        self.save()
