from processors.processor import Processor
from utils.supported_languages import SupportedLanguage


class Validator(Processor):
    def __init__(self, youtube_language: SupportedLanguage, model: str):
        super().__init__(youtube_language=youtube_language)
        self.validator_model = model

    def validate(self):
        pass
