from abc import ABC, abstractmethod


class Transcriber(ABC):
    def __init__(self, audio_path: str):
        self.audio_path = audio_path

    @abstractmethod
    def transcribe(self) -> str:
        pass