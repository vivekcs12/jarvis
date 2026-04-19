from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np

model = WhisperModel("tiny")

def listen():
    try:
        fs = 16000
        audio = sd.rec(int(3 * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()
        audio = audio / max(abs(audio))
        segments, _ = model.transcribe(audio.flatten())
        text = "".join([seg.text for seg in segments])
        return text.lower()
    except:
        return ""
