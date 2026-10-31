import sys

from PySide6.QtWidgets import QApplication

from assistant.ui.bubble import Bubble
from assistant.ui.chat_window import ChatWindow
from assistant.ui.tray import SystemTray
from assistant.ui.settings_window import SettingsWindow

app = QApplication(sys.argv)

app.setQuitOnLastWindowClosed(False)

bubble = Bubble()
chat = ChatWindow()
settings = SettingsWindow()

tray = SystemTray(chat, settings)

bubble.double_clicked.connect(chat.show)

bubble.show()

sys.exit(app.exec())
