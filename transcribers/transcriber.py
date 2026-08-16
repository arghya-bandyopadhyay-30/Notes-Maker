from abc import ABC, abstractmethod


class Transcriber(ABC):
    def __init__(self):
        self.audio_path = "audio_path"

    @abstractmethod
    def transcribe(self) -> str:
        pass