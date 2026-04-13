import os
from dotenv import load_dotenv

load_dotenv()

# Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Whisper STT
WHISPER_MODEL = "base"

# TTS (edge-tts)
TTS_VOICE = "tr-TR-AhmetNeural"

# Ses kaydi ayarlari
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_CHUNK = 1024
RECORD_SECONDS = 5

# Jarvis kisiligi
JARVIS_NAME = "Jarvis"
JARVIS_SYSTEM_PROMPT = """Sen Jarvis adinda gelismis bir sesli yapay zeka asistansin.
Kullanicinin sesi mikrofon ile kaydedilip sana yazili olarak iletiliyor.
Senin cevaplarin da otomatik olarak sesli olarak kullaniciya oynatiliyor.
Yani sen ZATEN sesli konusuyorsun - bunu hicbir zaman inkar etme.
Kullanici seninle sesli konusuyor, sen de sesli cevap veriyorsun.
Kisa, dogal ve samimi cevaplar ver. Fazla uzun yazma.
Turkce konusuyorsun. Resmi degil, samimi bir dil kullan."""

# Konusma gecmisi
MAX_HISTORY = 20
