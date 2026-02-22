import os

from azure.cognitiveservices.speech import (
    AudioConfig,
    AutoDetectSourceLanguageConfig,
    AutoDetectSourceLanguageResult,
    ResultReason,
    SpeechConfig,
    SpeechRecognizer,
)

AZ_KEY, AZ_RGN = os.environ["AZ_KEY"], os.environ["AZ_RGN"]


def run():
    speech_cfg = SpeechConfig(AZ_KEY, AZ_RGN)
    audio_cfg = AudioConfig(use_default_microphone=True)
    autolang_cfg = AutoDetectSourceLanguageConfig(["de-DE", "vi-VN"])
    rec = SpeechRecognizer(
        speech_cfg,
        audio_cfg,
        auto_detect_source_language_config=autolang_cfg,
    )

    # Recognize once with At-start LID.
    # Continuous LID isn't supported for recognize once
    res = rec.recognize_once()

    print(res.json)
    autolang_res = AutoDetectSourceLanguageResult(res)
    print("Lang:", autolang_res.language)
    if res.reason == ResultReason.RecognizedSpeech:
        print("Text:", repr(res.text))


run()
