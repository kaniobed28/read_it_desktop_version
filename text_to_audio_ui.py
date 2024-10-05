from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class TextToAudioUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Audio Converter")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #f5f5f5;")  # Set a light background color

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title Label
        title_label = QLabel("Text to Audio Converter")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Text Input Section
        layout.addWidget(QLabel("Enter Text:"))
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Type your text here...")
        self.text_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.text_edit)

        # Number of Loops
        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("Number of Loops:"))
        self.loop_spin = QSpinBox()
        self.loop_spin.setRange(1, 1000)
        self.loop_spin.setValue(1)
        loop_layout.addWidget(self.loop_spin)
        layout.addLayout(loop_layout)

        # Playback Speed
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Playback Speed (Words per Minute):"))
        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(50, 300)
        self.speed_spin.setValue(200)
        speed_layout.addWidget(self.speed_spin)
        layout.addLayout(speed_layout)

        # Language Selection
        layout.addWidget(QLabel("Select Language:"))
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        layout.addWidget(self.language_combo)

        # Control Buttons
        button_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
