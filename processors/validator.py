from processors.processor import Processor
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguage


class Validator(Processor):
    def __init__(self, youtube_language: SupportedLanguage, model: str, environment_system: EnvironmentSystem):
        super().__init__(youtube_language=youtube_language, model=model)
        self.validator_model = model
        environment_system.ensure_ollama_model(model)

    def validate(self):
        pass
