import os
import uuid
import tempfile
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMessageBox  # Add this import
import pyttsx3
from audio_utils import generate_audio_file
from text_to_audio_ui import TextToAudioUI

class TextToAudioApp(TextToAudioUI):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.current_loop = 0
        self.total_loops = 0
        self.generated_files = []

        # Initialize pyttsx3 engine
        self.engine = pyttsx3.init()
        
        self.populate_languages()

        # Connect signals
        self.play_button.clicked.connect(self.play_audio)
        self.stop_button.clicked.connect(self.stop_audio)

    def populate_languages(self):
        voices = self.engine.getProperty('voices')
        self.voice_map = {}
        for voice in voices:
            language = voice.languages[0] if voice.languages else "Unknown Language"
            language_name = f"{language} - {voice.name}"
            self.language_combo.addItem(language_name)
            self.voice_map[language_name] = voice

    def play_audio(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter some text.")
            return

        loops = self.loop_spin.value()
        speed = self.speed_spin.value()
        selected_language = self.language_combo.currentText()
        selected_voice = self.voice_map.get(selected_language)

        if selected_voice:
            self.engine.setProperty('voice', selected_voice.id)
            self.engine.setProperty('rate', speed)

        audio_file = generate_audio_file(self.engine, text)
        if not audio_file or not os.path.exists(audio_file):
            QMessageBox.critical(self, "Error", "Failed to generate audio.")
            return

        self.total_loops = loops
        self.current_loop = 0

        self.player.mediaStatusChanged.connect(self.handle_media_status)
        self.player.error.connect(self.handle_player_error)

        url = QUrl.fromLocalFile(os.path.abspath(audio_file))
        self.player.setMedia(QMediaContent(url))
        self.player.play()

        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_audio(self):
        self.player.stop()
        self.player.mediaStatusChanged.disconnect(self.handle_media_status)
        self.player.error.disconnect(self.handle_player_error)
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.current_loop += 1
            if self.current_loop < self.total_loops:
                self.player.stop()
                self.player.play()
            else:
                self.player.mediaStatusChanged.disconnect(self.handle_media_status)
                self.player.error.disconnect(self.handle_player_error)
                QMessageBox.information(self, "Playback Finished", "Audio playback completed.")
                self.play_button.setEnabled(True)
                self.stop_button.setEnabled(False)

    def handle_player_error(self, error):
        if error != QMediaPlayer.NoError:
            error_string = self.player.errorString()
            QMessageBox.critical(self, "Playback Error", f"Error: {error_string}")
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def closeEvent(self, event):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()

        event.accept()
