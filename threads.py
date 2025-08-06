from PyQt5.QtCore import QThread, pyqtSignal
import requests
from config import API_URL, LANGUAGE_MAP

class WorkerThread(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, prompt_text):
        super().__init__()
        self.prompt_text = prompt_text

    def run(self):
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{"parts": [{"text": self.prompt_text}]}]
            }
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            ai_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            ai_text = f"Error: {str(e)}"
        self.response_signal.emit(ai_text)

class DictionaryThread(QThread):
    definition_signal = pyqtSignal(str, str)

    def __init__(self, text, language):
        super().__init__()
        self.text = text
        self.language = language

    def run(self):
        try:
            target_language = LANGUAGE_MAP.get(self.language, "English")
            if ' ' in self.text.strip():
                prompt = f"In {target_language}, provide a clear explanation of the phrase or sentence '{self.text}' including: 1) its meaning, 2) the context in which it is typically used, and 3) an example sentence or phrase using it in a similar context. Keep the response concise, under 100 words."
            else:
                prompt = f"In {target_language}, provide a clear explanation of the word '{self.text}' including: 1) its definition, 2) its part of speech, 3) the context in which it is typically used, and 4) an example sentence using it. Keep the response concise, under 100 words."
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            if "candidates" in response_data and response_data["candidates"]:
                explanation = response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                explanation = "Error: No valid response from API"
        except requests.exceptions.RequestException as e:
            explanation = f"Network Error: {str(e)}"
        except KeyError as e:
            explanation = f"API Response Error: Invalid response format ({str(e)})"
        except Exception as e:
            explanation = f"Error: {str(e)}"
        self.definition_signal.emit(self.text, explanation)