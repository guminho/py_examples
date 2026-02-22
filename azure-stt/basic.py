import os

from azure.cognitiveservices.speech import (
    AudioConfig,
    CancellationReason,
    ResultReason,
    SpeechConfig,
    SpeechRecognizer,
)

AZ_KEY, AZ_RGN = os.environ["AZ_KEY"], os.environ["AZ_RGN"]


def run():
    speech_cfg = SpeechConfig(AZ_KEY, AZ_RGN)
    speech_cfg.speech_recognition_language = "vi-VN"
    audio_cfg = AudioConfig(use_default_microphone=True)
    rec = SpeechRecognizer(speech_cfg, audio_cfg)

    res = rec.recognize_once()

    print(res.json)
    if res.reason == ResultReason.RecognizedSpeech:
        print("Text:", repr(res.text))
    elif res.reason == ResultReason.NoMatch:
        print("Empty:", res.no_match_details)
    elif res.reason == ResultReason.Canceled:
        canceled = res.cancellation_details
        if canceled.reason == CancellationReason.Error:
            print("Error:", canceled.error_details)
        else:
            print("Canceled:", canceled.reason)


run()
