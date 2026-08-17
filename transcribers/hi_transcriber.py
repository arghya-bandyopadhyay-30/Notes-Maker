from faster_whisper import WhisperModel

from transcribers.process_segment import process_segment
from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguage


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
            language=SupportedLanguage.HINDI
        )

        transcript = [
            process_segment(segment)
            for segment in segments
        ]

        return "\n".join(transcript)
