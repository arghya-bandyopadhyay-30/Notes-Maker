from abc import ABC

from utils.supported_languages import SupportedLanguage


class Processor(ABC):
    def __init__(self, youtube_language: SupportedLanguage, model: str):
        self.youtube_language = youtube_language
        self.should_process = self.should_process()
        self.model = model

    def should_process(self) -> bool:
        return not (self.youtube_language == SupportedLanguage.ENGLISH)
