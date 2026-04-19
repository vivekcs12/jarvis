from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import time

model = WhisperModel("tiny")

def listen(threshold=0.01, silence_duration=1.5, fs=16000):
    try:
        print("Listening...")

        audio_data = []
        silence_start = None

        # Generator for audio blocks
        def callback(indata, frames, time, status):
            if status:
                print(status)
            audio_data.extend(indata.flatten())

        stream = sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback)
        with stream:
            while True:
                time.sleep(0.1)

                # Wait until we have some audio
                if not audio_data:
                    continue

                # Check if the last ~0.1 seconds of audio is mostly silent
                recent_samples = audio_data[-int(0.1 * fs):]
                if len(recent_samples) > 0:
                    volume = np.max(np.abs(recent_samples))

                    if volume < threshold:
                        if silence_start is None:
                            silence_start = time.time()
                        elif time.time() - silence_start > silence_duration:
                            # If we have enough data (at least 0.5s), stop listening
                            if len(audio_data) > fs * 0.5:
                                break
                            else:
                                # Too short, reset and keep listening
                                audio_data.clear()
                                silence_start = None
                    else:
                        silence_start = None

        print("Processing audio...")
        audio = np.array(audio_data, dtype='float32')
        # Normalize
        if len(audio) > 0 and max(abs(audio)) > 0:
            audio = audio / max(abs(audio))

        segments, _ = model.transcribe(audio)
        text = "".join([seg.text for seg in segments])
        return text.lower().strip()
    except Exception as e:
        print(f"Error in listen: {e}")
        return ""

if __name__ == "__main__":
    print(listen())
