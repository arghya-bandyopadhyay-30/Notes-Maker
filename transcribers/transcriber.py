from abc import ABC, abstractmethod

from utils.download_audio import download_audio_as_mp3
from utils.environment_system import EnvironmentSystem


class Transcriber(ABC):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        self.audio_path = download_audio_as_mp3(url=url, environment_system=environment_system)

    @abstractmethod
    def transcribe(self) -> str:
        pass