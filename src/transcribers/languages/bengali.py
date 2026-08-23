from banglaspeech2text import Speech2Text

from src.transcribers.base import Transcriber
from src.transcribers.segment import process_segment


class BengaliTranscriber(Transcriber):
    def load_model(self):
        return Speech2Text("small")

    def transcribe(self) -> str:
        segments = self.speech_to_text_model.recognize(
            self.audio_path,
            return_segments=True
        )

        transcript = [
            process_segment(segment)
            for segment in segments
        ]

        return "\n".join(transcript)
