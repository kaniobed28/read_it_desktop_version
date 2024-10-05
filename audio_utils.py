import os
import uuid
import tempfile
import pyttsx3

def generate_audio_file(engine, text):
    try:
        unique_filename = f"output_audio_{uuid.uuid4().hex}.wav"
        audio_file_path = os.path.join(tempfile.gettempdir(), unique_filename)

        engine.save_to_file(text, audio_file_path)
        engine.runAndWait()

        return audio_file_path
    except Exception as e:
        print(f"Audio Generation Error: {e}")
        return None
