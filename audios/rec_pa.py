import time
import wave

import pyaudio

duration = 3.5  # seconds
rate = 16000
bsize = int(rate * 0.2)
fmt = pyaudio.paInt16

with wave.open("output.wav", "wb") as wf:
    wf.setframerate(rate)
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.get_sample_size(fmt))

    def callback(indata, frames, tminfo, status):
        wf.writeframes(indata)
        return None, 0

    pya = pyaudio.PyAudio()
    stream = pya.open(
        rate=rate,
        channels=1,
        format=fmt,
        input=True,
        frames_per_buffer=bsize,
        stream_callback=callback,
    )

    print("recording...")
    time.sleep(duration)
    print("done")

    stream.stop_stream()
    stream.close()
    pya.terminate()
