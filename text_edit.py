from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal

class ClickableTextEdit(QTextEdit):
    text_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            cursor = self.textCursor()
            selected_text = cursor.selectedText().strip()
            if selected_text:
                clean_text = ''.join(c for c in selected_text if c.isalnum() or c.isspace())
                if clean_text:
                    self.text_clicked.emit(clean_text)
        super().mouseReleaseEvent(event)