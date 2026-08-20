import re
from typing import Final

from ollama import chat

from processors.base_models.translated_sentence import TranslatedSentence
from processors.processor import Processor
from prompt_factory.prompt_factory import PromptFactory
from utils.environment_system import EnvironmentSystem
from utils.string_constants import SENTENCE_BOUNDARY_PATTERN
from utils.supported_languages import SupportedLanguage

SENTENCE_PATTERN : Final[re.Pattern[str]] = re.compile(
    SENTENCE_BOUNDARY_PATTERN
)

class Translator(Processor):
    def __init__(self, youtube_language: SupportedLanguage, model: str, prompt_factory: PromptFactory, environment_system: EnvironmentSystem):
        super().__init__(
            youtube_language=youtube_language,
            model=model,
            prompt_factory=prompt_factory,
            environment_system=environment_system
        )
        self.split_sentences = lambda script: [
            sentence.strip()
            for sentence in SENTENCE_PATTERN.split(
                " ".join(script.split())
            )
            if sentence.strip()
        ]

    def translate(self, original_script: str) -> str:
        if not self.should_process():
            return original_script

        print(
            f"Translating the {self.youtube_language.value} script to English..."
        )

        prompts = [
            self.prompt_factory.prompt(
                prompt_file="translation_prompt.yaml",
                prompt_key="translation",
                placeholders={
                    "source_language": self.youtube_language.value,
                    "sentence": sentence,
                    "parsed_format": self.parser_format(
                        TranslatedSentence
                    ),
                },
            )
            for sentence in self.split_sentences(original_script)
        ]

        responses = [
            chat(
                model=self.model,
                messages=[
                    {
                        "role": item.role,
                        "content": item.prompt,
                    }
                    for item in prompt.content
                ],
                format=TranslatedSentence.model_json_schema(),
            )
            for prompt in prompts
        ]

        formatted_response = [
            TranslatedSentence.model_validate_json(
                response.message.content
            )
            for response in responses
        ]

        return " ".join(
            translated_sentence.text
            for translated_sentence in formatted_response
        )
