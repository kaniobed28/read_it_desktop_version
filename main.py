import sys
from PyQt5.QtWidgets import QApplication
from text_to_audio_app import TextToAudioApp

def main():
    app = QApplication(sys.argv)
    window = TextToAudioApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
