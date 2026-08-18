from processors.processor import Processor
from prompt_factory.prompt_factory import PromptFactory
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguage


class Translator(Processor):
    def __init__(self, youtube_language: SupportedLanguage, model: str, prompt_factory: PromptFactory, environment_system: EnvironmentSystem):
        super().__init__(youtube_language=youtube_language, model=model, prompt_factory=prompt_factory)
        self.translator_model = model
        environment_system.ensure_ollama_model(model)

    def translate(self, script: str) -> str:
        pass
