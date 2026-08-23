import whisper

from src.transcribers.base import Transcriber


class EnglishTranscriber(Transcriber):
    def load_model(self):
        return whisper.load_model("small")

    def transcribe(self) -> str:
        result = self.speech_to_text_model.transcribe(
            audio=self.audio_path,
            fp16=False,
            verbose=True
        )

        return result["text"].strip()
