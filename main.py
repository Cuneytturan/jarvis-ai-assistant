import os
import asyncio
import tempfile
import wave
import pyaudio
import whisper
import edge_tts
import pygame
from agent import run_agent
from config import (
    WHISPER_MODEL, TTS_VOICE, TTS_RATE,
    AUDIO_SAMPLE_RATE, AUDIO_CHANNELS,
    AUDIO_CHUNK, RECORD_SECONDS
)

WAKE_WORDS = ["hey jarvis", "jarvis", "hey cervis", "cervis"]

def record_audio(duration=RECORD_SECONDS):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=AUDIO_CHANNELS,
                    rate=AUDIO_SAMPLE_RATE, input=True, frames_per_buffer=AUDIO_CHUNK)
    frames = []
    for _ in range(0, int(AUDIO_SAMPLE_RATE / AUDIO_CHUNK * duration)):
        frames.append(stream.read(AUDIO_CHUNK))
    stream.stop_stream(); stream.close(); p.terminate()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf = wave.open(tmp.name, 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(AUDIO_SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return tmp.name

_whisper_model = None
def transcribe(audio_path):
    global _whisper_model
    if _whisper_model is None:
        print("Whisper model yukleniyor...")
        _whisper_model = whisper.load_model(WHISPER_MODEL)
    result = _whisper_model.transcribe(audio_path, language="tr")
    return result["text"].strip()

async def speak_async(text):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    communicate = edge_tts.Communicate(text, voice=TTS_VOICE, rate=TTS_RATE)
    await communicate.save(tmp.name)
    return tmp.name

def speak(text):
    print(f"Jarvis: {text}")
    audio_file = asyncio.run(speak_async(text))
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.unlink(audio_file)

def has_wake_word(text):
    t = text.lower()
    return any(w in t for w in WAKE_WORDS)

def remove_wake_word(text):
    t = text.lower()
    for w in WAKE_WORDS:
        t = t.replace(w, "").strip(" ,.")
    return t

def main():
    history = []
    print("=" * 50)
    print("  JARVIS AI AGENT - Hazir!")
    print("  'Hey Jarvis' diyerek baslayin")
    print("  Ctrl+C ile durdurun")
    print("=" * 50)
    speak("Hazir efendim.")

    while True:
        try:
            print("\nDinliyorum...")
            audio_path = record_audio()
            text = transcribe(audio_path)
            os.unlink(audio_path)
            if not text:
                continue
            print(f"Duydum: {text}")
            if has_wake_word(text):
                command = remove_wake_word(text)
                if not command:
                    speak("Evet?")
                    audio_path2 = record_audio()
                    command = transcribe(audio_path2)
                    os.unlink(audio_path2)
                    print(f"Komut: {command}")
                if command:
                    reply, history = run_agent(command, history)
                    speak(reply)
        except KeyboardInterrupt:
            speak("Kapatiyorum.")
            break
        except Exception as e:
            print(f"Hata: {e}")
            continue

if __name__ == "__main__":
    main()
