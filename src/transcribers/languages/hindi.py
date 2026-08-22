from faster_whisper import WhisperModel

from src.transcribers.segment import process_segment
from src.transcribers.base import Transcriber
from src.utils.environment import EnvironmentSystem
from src.utils.languages import SupportedLanguages


class HiTranscriber(Transcriber):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        super().__init__(url=url, environment_system=environment_system)
        self.speech_to_text_model = WhisperModel(
            "collabora/faster-whisper-small-hindi",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self) -> str:
        segments, info = self.speech_to_text_model.transcribe(
            self.audio_path,
            language=SupportedLanguages.HINDI
        )

        transcript = [
            process_segment(segment)
            for segment in segments
        ]

        return "\n".join(transcript)
