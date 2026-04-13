import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"
WHISPER_MODEL = "base"
TTS_VOICE = "tr-TR-AhmetNeural"
TTS_RATE = "+30%"  # Konusma hizi: +30% daha hizli
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_CHUNK = 1024
RECORD_SECONDS = 5
JARVIS_NAME = "Jarvis"
JARVIS_SYSTEM_PROMPT = """Sen Jarvis adinda bir AI agentsin. Sesli asistan olarak calisiyorsun.
KURALLAR:
- Cevaplarin MAKSIMUM 1-2 cumle olmali. Hic uzatma.
- Gorev verildiginde HEMEN yap, aciklama yapma.
- Yaptigin seyi tek cumlede bildir: "Tamam, yapildi." veya "Chrome acildi." gibi.
- Emin olamazsan sadece sor: "Hangisini istiyorsunuz?" gibi kisa sor.
- Ozur dileme, alternatif sunma, secenek listeleme YASAK.
- Soru soruldugunda normal ve mantikli cevap verebilirsin.
- Turkce konusuyorsun."""
MAX_HISTORY = 20
