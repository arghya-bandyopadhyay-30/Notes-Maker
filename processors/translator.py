from processors.processor import Processor
from utils.supported_languages import SupportedLanguage


class Translator(Processor):
    def __init__(self, youtube_language: SupportedLanguage, model: str):
        super().__init__(youtube_language=youtube_language)
        self.translator_model = model

    def translate(self):
        pass
