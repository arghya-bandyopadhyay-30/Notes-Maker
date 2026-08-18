from abc import ABC

from prompt_factory.prompt_factory import PromptFactory
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguage


class Processor(ABC):
    def __init__(self, youtube_language: SupportedLanguage, model: str, prompt_factory: PromptFactory, environment_system: EnvironmentSystem):
        self.youtube_language = youtube_language
        self.model = model
        environment_system.ensure_ollama_model(model)
        self.prompt_factory = prompt_factory

    def should_process(self) -> bool:
        return not (self.youtube_language == SupportedLanguage.ENGLISH)
