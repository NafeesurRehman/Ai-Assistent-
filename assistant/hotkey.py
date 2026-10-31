
import ctypes
import ctypes.wintypes

from PySide6.QtCore import QObject, QAbstractNativeEventFilter
from PySide6.QtWidgets import QApplication


WM_HOTKEY = 0x0312


class HotkeyFilter(QAbstractNativeEventFilter):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def nativeEventFilter(self, event_type, message):

        msg = ctypes.cast(
            int(message),
            ctypes.POINTER(ctypes.wintypes.MSG)
        ).contents

        if msg.message == WM_HOTKEY:
            self.callback()
            return True, 0

        return False, 0


class GlobalHotkey(QObject):

    def __init__(self, chat):
        super().__init__()

        self.chat = chat
        self.user32 = ctypes.windll.user32
        self.filter = HotkeyFilter(self.show_chat)
        self.registered = False

    def show_chat(self):

        self.chat.show()
        self.chat.activateWindow()
        self.chat.raise_()

    def register(self, shortcut="Ctrl + Shift + Space"):

        self.unregister()

        # Normalize shortcut format
        shortcut = shortcut.lower().replace(" ", "")

        shortcuts = {
            "ctrl+shift+space": (0x0002 | 0x0004, 0x20),
            "ctrl+alt+a": (0x0002 | 0x0001, 0x41)
        }

        if shortcut not in shortcuts:
            print("Unsupported shortcut:", shortcut)
            return False

        modifiers, key = shortcuts[shortcut]

        success = self.user32.RegisterHotKey(
            None, 1, modifiers, key
        )

        if not success:
            print("Hotkey registration failed!")
            return False

        QApplication.instance().installNativeEventFilter(
            self.filter
        )

        self.registered = True

        print("Hotkey registered:", shortcut)

        return True

    def unregister(self):

        if self.registered:

            QApplication.instance().removeNativeEventFilter(
                self.filter
            )

            self.user32.UnregisterHotKey(None, 1)
            self.registered = False

    def __del__(self):

        try:
            self.unregister()
        except Exception:
            pass
        