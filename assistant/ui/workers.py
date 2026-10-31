
import time

from PySide6.QtCore import QThread, Signal
from assistant.ai_engine import get_ai_response


class AIWorker(QThread):

    finished_response = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):

        for attempt in range(3):

            try:
                response = get_ai_response(self.message)

                if not response:
                    response = "No response received."

                if "503" in str(response) and attempt < 2:
                    time.sleep(2)
                    continue

                self.finished_response.emit(str(response))
                return

            except Exception as error:

                error_text = str(error)

                if ("503" in error_text or "UNAVAILABLE" in error_text) and attempt < 2:
                    time.sleep(3)
                    continue

                self.error_occurred.emit(error_text)
                return

        self.error_occurred.emit(
            "Gemini server is busy. Please try again later."
        )