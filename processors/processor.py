from abc import ABC

from prompt_factory.prompt_factory import PromptFactory
from utils.supported_languages import SupportedLanguage


class Processor(ABC):
    def __init__(self, youtube_language: SupportedLanguage, model: str, prompt_factory: PromptFactory):
        self.youtube_language = youtube_language
        self.should_process = self.should_process()
        self.model = model
        self.prompt_factory = prompt_factory

    def should_process(self) -> bool:
        return not (self.youtube_language == SupportedLanguage.ENGLISH)
