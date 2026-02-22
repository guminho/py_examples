# apt install portaudio19-dev
import wave

import sounddevice as sd

rate = 16000
bsize = int(rate * 0.064)
fmt = "int16"

with wave.open("output.wav", "wb") as wf:
    wf.setframerate(rate)
    wf.setnchannels(1)
    wf.setsampwidth(2)

    def cb(indata, frames, tminfo, status):
        wf.writeframes(bytes(indata))

    with sd.RawInputStream(rate, bsize, channels=1, dtype=fmt, callback=cb):
        input("Enter to stop..")
