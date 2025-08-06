from PyQt5.QtWidgets import QDialog, QTextEdit, QPushButton, QVBoxLayout

class ExplanationDialog(QDialog):
    def __init__(self, text, explanation, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Explanation: {text}")
        self.setStyleSheet("background-color: #f5f5f5;")
        self.setGeometry(150, 150, 400, 300)
        self.init_ui(text, explanation)

    def init_ui(self, text, explanation):
        layout = QVBoxLayout()
        explanation_text = QTextEdit()
        explanation_text.setReadOnly(True)
        explanation_text.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        explanation_text.setText(f"<b>{text}</b>: {explanation}")
        layout.addWidget(explanation_text)
        close_button = QPushButton("Close")
        close_button.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 10px; border-radius: 5px;")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        self.setLayout(layout)