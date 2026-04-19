import speech_recognition as sr
from faster_whisper import WhisperModel
import numpy as np
import io
import wave

# Load the local tiny model
model = WhisperModel("tiny")

# Initialize the recognizer
recognizer = sr.Recognizer()
# Adjust for background noise automatically
recognizer.dynamic_energy_threshold = True

def listen():
    with sr.Microphone(sample_rate=16000) as source:
        print("\nAdjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        try:
            # Listen for user input. It will stop automatically when you stop speaking.
            # Timeout is how long it waits for you to START speaking.
            # phrase_time_limit is the maximum length of a single phrase.
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=30)

            print("Processing audio...")

            # Convert SpeechRecognition AudioData to numpy array for Whisper
            raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
            # The data is 16-bit PCM. Convert it to float32 between -1.0 and 1.0
            audio_np = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0

            segments, _ = model.transcribe(audio_np)
            text = "".join([seg.text for seg in segments])
            return text.lower().strip()

        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return ""
        except Exception as e:
            print(f"Error in listen: {e}")
            return ""

if __name__ == "__main__":
    print(listen())
