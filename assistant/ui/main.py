import sys
from PySide6.QtWidgets import QApplication
from assistant.ui.bubble import Bubble

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    bubble = Bubble()
    bubble.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()