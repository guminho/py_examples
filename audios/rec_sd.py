import time
import wave

import sounddevice as sd

duration = 3.5  # seconds
rate = 16000
bsize = int(rate * 0.2)
fmt = "int16"

with wave.open("output.wav", "wb") as wf:
    wf.setframerate(rate)
    wf.setnchannels(1)
    wf.setsampwidth(2)

    def callback(indata, frames, tminfo, status):
        wf.writeframes(bytes(indata))

    stream = sd.RawInputStream(rate, bsize, channels=1, dtype=fmt, callback=callback)

    with stream:
        print("recording...")
        time.sleep(duration)
        print("done")
