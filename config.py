import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"
WHISPER_MODEL = "base"
TTS_VOICE = "tr-TR-AhmetNeural"
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_CHUNK = 1024
RECORD_SECONDS = 5
JARVIS_NAME = "Jarvis"
JARVIS_SYSTEM_PROMPT = "Sen Jarvis adinda gelismis bir AI asistansin. Turkce konusuyorsun."
MAX_HISTORY = 20
