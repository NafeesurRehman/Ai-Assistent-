
from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QSystemTrayIcon,
    QStyle
)


class SystemTray:

    def __init__(self, chat, settings):

        self.chat = chat
        self.settings = settings

        icon = QApplication.style().standardIcon(
            QStyle.StandardPixmap.SP_ComputerIcon
        )

        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip("AI Assistant")

        self.menu = QMenu()

        open_action = self.menu.addAction("Open AI Assistant")
        settings_action = self.menu.addAction("Settings")

        self.menu.addSeparator()

        exit_action = self.menu.addAction("Exit")

        open_action.triggered.connect(self.open_chat)
        settings_action.triggered.connect(self.open_settings)
        exit_action.triggered.connect(self.exit_app)

        self.tray.setContextMenu(self.menu)

        self.tray.activated.connect(self.on_tray_activated)

        self.tray.show()

    def open_chat(self):

        self.chat.show()
        self.chat.activateWindow()
        self.chat.raise_()

    def open_settings(self):

        self.settings.show()
        self.settings.activateWindow()
        self.settings.raise_()

    def on_tray_activated(self, reason):

        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_chat()

    def exit_app(self):

        self.tray.hide()
        QApplication.quit()