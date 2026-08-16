from banglaspeech2text import Speech2Text

from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem


class BnTranscriber(Transcriber):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        super().__init__(url=url, environment_system=environment_system)
        self.speech_to_text_model = Speech2Text("small")

    def transcribe(self) -> str:
        segments = self.speech_to_text_model.recognize(
            self.audio_path,
            return_segments=True
        )

        transcript = [
            segment.text.strip()
            for segment in segments
        ]

        return "\n".join(transcript)
