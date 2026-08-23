from banglaspeech2text import Speech2Text

from src.transcribers.segment import process_segment
from src.transcribers.transcriber import Transcriber
from src.utils.formatting.strings import WHISPER_MODEL_SMALL


class BengaliTranscriber(Transcriber):
    def load_model(self) -> Speech2Text:
        return Speech2Text(WHISPER_MODEL_SMALL)

    def transcribe(self) -> str:
        segments = self.speech_to_text_model.recognize(self.audio_path, return_segments=True)

        transcript = [process_segment(segment) for segment in segments]

        return "\n".join(transcript)
