from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QComboBox, QHBoxLayout, QLineEdit, QListWidget
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from text_edit import ClickableTextEdit
from threads import WorkerThread, DictionaryThread
from dialog import ExplanationDialog

class TextToAudioUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Read It by Obed KANI")
        self.setGeometry(100, 100, 500, 800)  # Increased height for history panel
        self.setStyleSheet("background-color: #f5f5f5;")
        self.setWindowIcon(QIcon(r"C:\Users\PC\Desktop\new readit\image.png"))
        self.explanation_language = "English"
        self.history = []  # Store AI text and explanations
        self.explanation_dialog = None
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
        self.text_edit = ClickableTextEdit()
        self.text_edit.setPlaceholderText("Type your text here...")
        self.text_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
        self.text_edit.text_clicked.connect(self.handle_text_click)
        layout.addWidget(self.text_edit)

        # Prompt Input Section
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

        # Loading Indicator for AI Response
        self.loading_label = QLabel("Loading AI Response...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)

        # Loading Indicator for Explanations
        self.explanation_loading_label = QLabel("Loading Explanation...")
        self.explanation_loading_label.setAlignment(Qt.AlignCenter)
        self.explanation_loading_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        self.explanation_loading_label.setVisible(False)
        layout.addWidget(self.explanation_loading_label)

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

        # Language Selection (for text-to-speech)
        layout.addWidget(QLabel("Select Language:"))
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        layout.addWidget(self.language_combo)

        # Explanation Language Selection
        layout.addWidget(QLabel("Select Explanation Language:"))
        self.explanation_language_combo = QComboBox()
        self.explanation_language_combo.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        self.explanation_languages = ["English", "French", "Chinese"]
        for lang_name in self.explanation_languages:
            self.explanation_language_combo.addItem(lang_name)
        self.explanation_language_combo.currentIndexChanged.connect(self.change_explanation_language)
        layout.addWidget(self.explanation_language_combo)

        # Rollback Section
        rollback_layout = QHBoxLayout()
        rollback_layout.addWidget(QLabel("Rollback Seconds:"))
        self.rollback_spin = QSpinBox()
        self.rollback_spin.setRange(1, 60)
        self.rollback_spin.setValue(5)
        rollback_layout.addWidget(self.rollback_spin)

        self.rollback_button = QPushButton("Rollback")
        self.rollback_button.setEnabled(False)
        self.rollback_button.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 10px; border-radius: 5px;")
        rollback_layout.addWidget(self.rollback_button)
        layout.addLayout(rollback_layout)

        # Control Buttons
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

        # History Panel
        layout.addWidget(QLabel("History:"))
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")
        self.history_list.itemClicked.connect(self.display_history_item)
        layout.addWidget(self.history_list)

        clear_history_button = QPushButton("Clear History")
        clear_history_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px; border-radius: 5px;")
        clear_history_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_history_button)

        self.setLayout(layout)

    def get_ai_response(self):
        prompt_text = self.prompt_edit.text().strip()
        if prompt_text:
            self.loading_label.setVisible(True)
            self.generate_button.setEnabled(False)
            self.text_edit.clear()
            self.worker_thread = WorkerThread(prompt_text)
            self.worker_thread.response_signal.connect(self.display_ai_response)
            self.worker_thread.start()

    def display_ai_response(self, ai_text):
        self.loading_label.setVisible(False)
        self.text_edit.append(f"\n{ai_text}")
        self.generate_button.setEnabled(True)
        # Add to history
        self.history.append(f"Prompt: {self.prompt_edit.text()}\nResponse: {ai_text}")
        self.history_list.addItem(f"Prompt: {self.prompt_edit.text()}")

    def change_explanation_language(self, index):
        self.explanation_language = self.explanation_languages[index]

    def handle_text_click(self, text):
        if text:
            self.explanation_loading_label.setVisible(True)
            self.dictionary_thread = DictionaryThread(text, self.explanation_language)
            self.dictionary_thread.definition_signal.connect(self.show_definition)
            self.dictionary_thread.start()

    def show_definition(self, text, explanation):
        self.explanation_loading_label.setVisible(False)
        # Show in dialog
        self.explanation_dialog = ExplanationDialog(text, explanation, self)
        self.explanation_dialog.show()
        # Add to history
        self.history.append(f"Explanation: {text} - {explanation}")
        self.history_list.addItem(f"Explanation: {text}")

    def display_history_item(self, item):
        index = self.history_list.row(item)
        self.text_edit.setText(self.history[index])

    def clear_history(self):
        self.history_list.clear()
        self.history = []