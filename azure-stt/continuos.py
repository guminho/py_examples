import os
import time

from azure.cognitiveservices.speech import (
    AudioConfig,
    PropertyId,
    SpeechConfig,
    SpeechRecognizer,
)
from azure.cognitiveservices.speech.audio import AudioStreamFormat, PushAudioInputStream

AZ_KEY, AZ_RGN = os.environ["AZ_KEY"], os.environ["AZ_RGN"]


def run():
    speech_cfg = SpeechConfig(AZ_KEY, AZ_RGN)
    speech_cfg.speech_recognition_language = "vi-VN"
    istream = PushAudioInputStream(AudioStreamFormat(16000))
    audio_cfg = AudioConfig(stream=istream)
    rec = SpeechRecognizer(speech_cfg, audio_cfg)
    rec.properties.set_property(
        PropertyId.Speech_SegmentationSilenceTimeoutMs, "400"
    )  # '100'-'5000'ms, '500' default
    rec.properties.set_property(
        PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "30000"
    )  # '15000'ms default

    done = False

    def stop_cb(evt):
        print(f"DONE on {evt}")
        nonlocal done
        done = True

    rec.recognizing.connect(lambda evt: print(f"RECOGNIZING: {evt.result.text!r}"))
    rec.recognized.connect(lambda evt: print(f"RECOGNIZED: {evt.result.text!r}"))
    rec.session_stopped.connect(stop_cb)
    rec.canceled.connect(stop_cb)

    print("starting..")
    rec.start_continuous_recognition()
    with open("thoitiet.wav", "rb") as wf:
        wf.read(44)
        istream.write(wf.read())
    istream.close()
    while not done:
        time.sleep(0.2)
    rec.stop_continuous_recognition()


run()
