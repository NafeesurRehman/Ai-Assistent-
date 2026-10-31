
import markdown

from PySide6.QtWidgets import QTextBrowser
from PySide6.QtCore import QUrl


class MarkdownView(QTextBrowser):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setOpenExternalLinks(True)
        self.setStyleSheet("""
            QTextBrowser {
                background-color: #1f2937;
                color: #f9fafb;
                border: none;
                padding: 10px;
                font-size: 14px;
            }

            a {
                color: #60a5fa;
            }

            pre {
                background-color: #111827;
                color: #e5e7eb;
                padding: 12px;
                border-radius: 8px;
            }

            code {
                background-color: #374151;
                color: #93c5fd;
                padding: 3px;
                border-radius: 4px;
            }

            blockquote {
                border-left: 3px solid #4f8cff;
                padding-left: 10px;
                color: #9ca3af;
            }
        """)

    def set_markdown(self, text):

        html = markdown.markdown(
            text,
            extensions=[
                "fenced_code",
                "tables",
                "nl2br",
                "codehilite"
            ]
        )

        self.setHtml(html)