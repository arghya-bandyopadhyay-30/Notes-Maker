from faster_whisper import WhisperModel

from src.transcribers.transcriber import Transcriber
from src.utils.formatting.strings import (
    FASTER_WHISPER_COMPUTE_TYPE_INT8,
    FASTER_WHISPER_DEVICE_CPU,
    FASTER_WHISPER_HINDI_MODEL,
)
from src.utils.supported_languages import SupportedLanguages


class HindiTranscriber(Transcriber):
    def load_model(self) -> WhisperModel:
        return WhisperModel(
            FASTER_WHISPER_HINDI_MODEL,
            device=FASTER_WHISPER_DEVICE_CPU,
            compute_type=FASTER_WHISPER_COMPUTE_TYPE_INT8,
        )

    def transcribe(self) -> str:
        segments, info = self.speech_to_text_model.transcribe(
            self.audio_path, language=SupportedLanguages.HINDI
        )
        transcript = [self.process_segment(segment) for segment in segments]
        return "\n".join(transcript)
