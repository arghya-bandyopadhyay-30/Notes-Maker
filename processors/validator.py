from processors.processor import Processor
from prompt_factory.prompt_factory import PromptFactory
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguages


class Validator(Processor):
    def __init__(self, youtube_language: SupportedLanguages, model: str, prompt_factory: PromptFactory, environment_system: EnvironmentSystem):
        super().__init__(
            youtube_language=youtube_language,
            model=model,
            prompt_factory=prompt_factory,
            environment_system=environment_system
        )

    def validate(self, original_script: str, translated_script: str) -> float:
        if not self.should_process():
            return 1

        print(
            f"Validating the {self.youtube_language.value} script to English translated scrip..."
        )


        return 0
