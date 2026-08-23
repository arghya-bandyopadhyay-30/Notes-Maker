from abc import ABC, abstractmethod
from typing import TypeAlias

from banglaspeech2text import Speech2Text
from faster_whisper import WhisperModel
from whisper import Whisper

from src.utils.config.container import DependencyContainer
from src.utils.io.filesystem_ops import download_audio_as_wav

SpeechToTextModel: TypeAlias = Speech2Text | Whisper | WhisperModel

class Transcriber(ABC):
    def __init__(self, url: str, dependencies: DependencyContainer):
        self.file_system = dependencies.file_system
        self.audio_path = download_audio_as_wav(url=url, environment_system=dependencies.environment_system)
        self.speech_to_text_model = self.load_model()

    @abstractmethod
    def load_model(self) -> SpeechToTextModel:
        pass

    @abstractmethod
    def transcribe(self) -> str:
        pass

    def close(self) -> None:
        self.speech_to_text_model = None
        self.file_system.remove(self.audio_path)
