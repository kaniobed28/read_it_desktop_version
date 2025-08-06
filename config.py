import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API configuration
API_KEY = os.getenv("API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Language mapping for explanations
LANGUAGE_MAP = {
    "English": "English",
    "French": "French",
    "Chinese": "Chinese (Simplified)"
}