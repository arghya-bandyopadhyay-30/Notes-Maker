import whisper

from src.transcribers.base import Transcriber
from src.utils.io.environment import EnvironmentSystem


class EnTranscriber(Transcriber):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        super().__init__(url=url, environment_system=environment_system)
        self.speech_to_text_model = whisper.load_model("small")

    def transcribe(self) -> str:
        result = self.speech_to_text_model.transcribe(
            audio=self.audio_path,
            fp16=False,
            verbose=True
        )

        return result["text"].strip()
