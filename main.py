import os
import asyncio
import tempfile
import wave
import pyaudio
import whisper
import anthropic
import edge_tts
import pygame
from config import (
    ANTHROPIC_API_KEY, CLAUDE_MODEL, WHISPER_MODEL,
    TTS_VOICE, AUDIO_SAMPLE_RATE, AUDIO_CHANNELS,
    AUDIO_CHUNK, RECORD_SECONDS, JARVIS_SYSTEM_PROMPT, MAX_HISTORY
)

# --- Ses kaydi ---
def record_audio(duration=RECORD_SECONDS):
    print(f"Dinliyorum... ({duration} saniye)")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=AUDIO_SAMPLE_RATE,
        input=True,
        frames_per_buffer=AUDIO_CHUNK
    )
    frames = []
    for _ in range(0, int(AUDIO_SAMPLE_RATE / AUDIO_CHUNK * duration)):
        data = stream.read(AUDIO_CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf = wave.open(tmp.name, 'wb')
    wf.setnchannels(AUDIO_CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(AUDIO_SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return tmp.name

# --- STT: Whisper ---
def transcribe(audio_path):
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_path, language="tr")
    text = result["text"].strip()
    print(f"Sen: {text}")
    return text

# --- AI: Claude ---
def ask_claude(user_input, history):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    history.append({"role": "user", "content": user_input})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=JARVIS_SYSTEM_PROMPT,
        messages=history
    )
    reply = response.content[0].text
    history.append({"role": "assistant", "content": reply})
    print(f"Jarvis: {reply}")
    return reply, history

# --- TTS: edge-tts ---
async def speak_async(text):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    communicate = edge_tts.Communicate(text, voice=TTS_VOICE)
    await communicate.save(tmp.name)
    return tmp.name

def speak(text):
    audio_file = asyncio.run(speak_async(text))
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.unlink(audio_file)

# --- Ana dongu ---
def main():
    print("Jarvis hazir! Konusmak icin Enter'a basin, cikmak icin 'q' yazin.")
    history = []
    while True:
        cmd = input("\n[Enter=Konус | q=Cik] > ").strip().lower()
        if cmd == 'q':
            speak("Gorursunuz efendim.")
            break
        audio_path = record_audio()
        user_text = transcribe(audio_path)
        os.unlink(audio_path)
        if not user_text:
            print("Ses algilanamadi.")
            continue
        reply, history = ask_claude(user_text, history)
        speak(reply)

if __name__ == "__main__":
    main()
