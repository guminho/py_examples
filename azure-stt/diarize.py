import os
import time

from azure.cognitiveservices.speech import (
    AudioConfig,
    PropertyId,
    SessionEventArgs,
    SpeechConfig,
)
from azure.cognitiveservices.speech.transcription import (
    ConversationTranscriber,
    ConversationTranscriptionEventArgs,
)

AZ_KEY, AZ_RGN = os.environ["AZ_KEY"], os.environ["AZ_RGN"]


def rshorten(text: str, width: int = 80):
    return text if len(text) <= width else f"...{text[-width:]}"


def main():
    speech_cfg = SpeechConfig(AZ_KEY, AZ_RGN)
    speech_cfg.speech_recognition_language = "en-US"
    speech_cfg.set_property(
        property_id=PropertyId.SpeechServiceResponse_DiarizeIntermediateResults,
        value="true",
    )
    audio_cfg = AudioConfig(filename="katiesteve.wav")
    transcriber = ConversationTranscriber(speech_cfg, audio_cfg)

    done = False

    def on_stop(evt: SessionEventArgs):
        print(f"DONE on {evt}")
        nonlocal done
        done = True

    def on_chunk(e: ConversationTranscriptionEventArgs):
        print(f"chunk - <{e.result.speaker_id}>:{rshorten(e.result.text)!r}")

    def on_final(e: ConversationTranscriptionEventArgs):
        print(f"FINAL - <{e.result.speaker_id}>:{rshorten(e.result.text)!r}")

    transcriber.session_started.connect(lambda e: print("started"))
    transcriber.transcribing.connect(on_chunk)
    transcriber.transcribed.connect(on_final)
    transcriber.session_stopped.connect(on_stop)
    transcriber.canceled.connect(on_stop)

    transcriber.start_transcribing_async()
    while not done:
        time.sleep(0.5)
    transcriber.stop_transcribing_async()


main()
