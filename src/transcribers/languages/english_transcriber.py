import whisper
from whisper import Whisper

from src.transcribers.transcriber import Transcriber
from src.utils.formatting.strings import WHISPER_MODEL_SMALL


class EnglishTranscriber(Transcriber):
    def load_model(self) -> Whisper:
        return whisper.load_model(WHISPER_MODEL_SMALL)

    def transcribe(self) -> str:
        result = self.speech_to_text_model.transcribe(
            audio=self.audio_path, fp16=False, verbose=True
        )

        return result["text"].strip()
