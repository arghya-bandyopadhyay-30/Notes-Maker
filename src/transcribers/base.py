from abc import ABC, abstractmethod

from src.utils.filesystem import download_audio_as_wav
from src.utils.environment import EnvironmentSystem


class Transcriber(ABC):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        self.audio_path = download_audio_as_wav(url=url, environment_system=environment_system)

    @abstractmethod
    def transcribe(self) -> str:
        pass
