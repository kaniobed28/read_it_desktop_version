from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QComboBox, QHBoxLayout, QLineEdit, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import ollama 


class WorkerThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, prompt_text):
        super().__init__()
        self.prompt_text = prompt_text

    def run(self):
        try:
            # Simulate the AI response generation
            response = ollama.chat(model="mistral", messages=[{"role": "user", "content":  self.prompt_text}])
            ai_text = response["message"]["content"]
        except Exception as e:
            ai_text = f"Error: {str(e)}"
        self.response_signal.emit(ai_text)


class TextToAudioUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Read It by Obed KANI")
        self.setGeometry(100, 100, 500, 700)  # Adjusted height for new components
        self.setStyleSheet("background-color: #f5f5f5;")

        # Set the application icon
        self.setWindowIcon(QIcon(r"C:\Users\PC\Desktop\new readit\image.png"))  # Ensure the path is correct

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title Label
        title_label = QLabel("Text to Audio Converter with AI")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Text Input Section
        layout.addWidget(QLabel("Enter Text:"))
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Type your text here...")
        self.text_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.text_edit)

        # Prompt Input Section (New)
        layout.addWidget(QLabel("Enter AI Prompt:"))
        self.prompt_edit = QLineEdit()
        self.prompt_edit.setPlaceholderText("Type your prompt for the AI here...")
        self.prompt_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.prompt_edit)

        # Generate Response Button
        self.generate_button = QPushButton("Generate Response")
        self.generate_button.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 10px; border-radius: 5px;")
        self.generate_button.clicked.connect(self.get_ai_response)
        layout.addWidget(self.generate_button)

        # Loading Indicator (initially hidden)
        self.loading_label = QLabel("Loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)

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

        # Rollback Section
        rollback_layout = QHBoxLayout()
        rollback_layout.addWidget(QLabel("Rollback Seconds:"))
        self.rollback_spin = QSpinBox()
        self.rollback_spin.setRange(1, 60)  # Limit rollback to 60 seconds
        self.rollback_spin.setValue(5)  # Default rollback time
        rollback_layout.addWidget(self.rollback_spin)

        self.rollback_button = QPushButton("Rollback")
        self.rollback_button.setEnabled(False)
        self.rollback_button.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 10px; border-radius: 5px;")
        rollback_layout.addWidget(self.rollback_button)
        layout.addLayout(rollback_layout)

        # Control Buttons (Play, Pause, Stop)
        button_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("background-color: #FF9800; color: white; border: none; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px; border-radius: 5px;")
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_ai_response(self):
        prompt_text = self.prompt_edit.text().strip()  # Get the prompt from the new field
        if prompt_text:
            self.loading_label.setVisible(True)  # Show loading indicator
            self.generate_button.setEnabled(False)  # Disable generate button during processing

            # Clear previous response text
            self.text_edit.clear()

            # Create a worker thread to get the AI response
            self.worker_thread = WorkerThread(prompt_text)
            self.worker_thread.response_signal.connect(self.display_ai_response)
            self.worker_thread.start()

    def display_ai_response(self, ai_text):
        self.loading_label.setVisible(False)  # Hide loading indicator
        self.text_edit.append(f"\n{ai_text}")  # Append AI response to the text input box
        self.generate_button.setEnabled(True)  # Enable generate button after processing is done
