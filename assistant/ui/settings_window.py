
import json
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QCheckBox,
    QLineEdit, QGroupBox
)

from assistant.startup import enable_startup, disable_startup
from assistant.ai_engine import configure_ai


class SettingsWindow(QWidget):

    def __init__(self, chat, hotkey_manager):
        super().__init__()

        self.chat = chat
        self.hotkey_manager = hotkey_manager

        self.setWindowTitle("AI Assistant - Settings")
        self.resize(420, 580)

        self.settings_file = (
            Path(__file__).resolve().parents[2] / "settings.json"
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("AI Assistant Settings")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )
        layout.addWidget(title)

        # Appearance
        appearance = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout(appearance)

        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light"])

        appearance_layout.addWidget(QLabel("Theme"))
        appearance_layout.addWidget(self.theme)
        layout.addWidget(appearance)

        # AI Configuration
        ai_group = QGroupBox("AI Configuration")
        ai_layout = QVBoxLayout(ai_group)

        ai_layout.addWidget(QLabel("Gemini API Key"))

        self.api_key = QLineEdit()
        self.api_key.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.api_key.setPlaceholderText(
            "Enter your Gemini API key"
        )

        ai_layout.addWidget(self.api_key)
        ai_layout.addWidget(QLabel("Gemini Model"))

        self.model = QComboBox()
        self.model.addItems([
            "gemini-3.8-flash",
            "gemini-2.5-flash"
        ])

        ai_layout.addWidget(self.model)
        layout.addWidget(ai_group)

        # General
        general = QGroupBox("General")
        general_layout = QVBoxLayout(general)

        self.startup = QCheckBox("Start with Windows")
        general_layout.addWidget(self.startup)

        general_layout.addWidget(QLabel("Keyboard Shortcut"))

        self.hotkey_combo = QComboBox()
        self.hotkey_combo.addItems([
            "Ctrl + Shift + Space",
            "Ctrl + Alt + A"
        ])

        general_layout.addWidget(self.hotkey_combo)
        layout.addWidget(general)

        # Save
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(save_button)

        self.status = QLabel("")
        layout.addWidget(self.status)

        layout.addStretch()

        self.load_settings()

    def load_settings(self):

        try:
            data = {}

            if self.settings_file.exists():
                with open(
                    self.settings_file,
                    "r",
                    encoding="utf-8"
                ) as file:
                    data = json.load(file)

            self.theme.setCurrentText(
                data.get("theme", "Dark")
            )

            self.startup.setChecked(
                data.get("startup", False)
            )

            self.hotkey_combo.setCurrentText(
                data.get(
                    "hotkey",
                    "Ctrl + Shift + Space"
                )
            )

            self.model.setCurrentText(
                data.get("model", "gemini-3.8-flash")
            )

            self.api_key.setText(
                os.getenv("GEMINI_API_KEY", "")
            )

            self.chat.apply_theme(self.theme.currentText())

        except Exception as error:
            print("Settings load error:", error)
            self.status.setText("Could not load settings.")

    def save_settings(self):

        api_key = self.api_key.text().strip()

        data = {
            "theme": self.theme.currentText(),
            "startup": self.startup.isChecked(),
            "hotkey": self.hotkey_combo.currentText(),
            "model": self.model.currentText()
        }

        try:
            # Configure Gemini
            configure_ai(
                api_key=api_key,
                model=data["model"]
            )

            # Register hotkey before saving
            if self.hotkey_manager:
                shortcut = (
                    data["hotkey"]
                    .lower()
                    .replace(" ", "")
                )

                if not self.hotkey_manager.register(shortcut):
                    self.status.setText(
                        "Hotkey unavailable or already in use!"
                    )
                    return

            # Windows startup
            if data["startup"]:
                enable_startup()
            else:
                disable_startup()

            # Save settings (API key is NOT saved)
            with open(
                self.settings_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(data, file, indent=4)

            # Apply theme
            self.chat.apply_theme(data["theme"])

            self.status.setText(
                "Settings saved successfully!"
            )

        except Exception as error:

            self.status.setText(
                "Error saving settings!"
            )

            print("Settings error:", error)