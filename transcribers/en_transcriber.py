import whisper

from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem
from utils.process_segment import process_segment
from utils.supported_languages import SupportedLanguage


class EnTranscriber(Transcriber):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        super().__init__(url=url, environment_system=environment_system)
        speech_to_text_model = whisper.load_model("small")
        self.segments = speech_to_text_model.transcribe(
            self.audio_path,
            language=SupportedLanguage.ENGLISH.value,
            task="transcribe",
            fp16=False,
        )

    def transcribe(self) -> str:
        transcript = [
            process_segment(segment)
            for segment in self.segments["segments"]
        ]

        return "\n".join(transcript)
