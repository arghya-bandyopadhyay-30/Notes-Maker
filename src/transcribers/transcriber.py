from abc import ABC, abstractmethod

from banglaspeech2text import Speech2Text
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
from whisper import Whisper

from src.bootstrap.container import DependencyContainer
from src.transcribers.audio_downloader import download_audio_as_wav
from src.utils.formatting.strings import SEGMENT_PRINT_FORMAT

type SpeechToTextModel = Speech2Text | Whisper | WhisperModel


class Transcriber(ABC):
    def __init__(self, url: str, dependencies: DependencyContainer):
        self.file_system = dependencies.file_system
        self.audio_path = download_audio_as_wav(
            url=url, environment_system=dependencies.environment_system
        )
        self.speech_to_text_model = self.load_model()

    def process_segment(self, segment: Segment) -> str:
        text: str = segment.text.strip()
        print(SEGMENT_PRINT_FORMAT.format(segment.start, segment.end, text))
        return text

    @abstractmethod
    def load_model(self) -> SpeechToTextModel:
        pass

    @abstractmethod
    def transcribe(self) -> str:
        pass

    def close(self) -> None:
        self.speech_to_text_model = None
        self.file_system.remove(self.audio_path)
