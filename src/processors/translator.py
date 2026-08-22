import re
from typing import Final

from src.processors.base.models import TranslatedSegment
from src.processors.base.processor import Processor
from src.prompts.factory import PromptFactory
from src.utils.config import LLMConfig
from src.utils.strings import SENTENCE_BOUNDARY_PATTERN
from src.utils.languages import SupportedLanguages

SENTENCE_PATTERN : Final[re.Pattern[str]] = re.compile(
    SENTENCE_BOUNDARY_PATTERN
)

class Translator(Processor):
    def __init__(self, youtube_language: SupportedLanguages, llm: LLMConfig, prompt_factory: PromptFactory):
        super().__init__(
            youtube_language=youtube_language,
            llm=llm,
            prompt_factory=prompt_factory,
        )
        self.split_sentences = lambda script: [
            sentence.strip()
            for sentence in SENTENCE_PATTERN.split(
                " ".join(script.split())
            )
            if sentence.strip()
        ]

    async def translate(self, original_script: str) -> str:
        if not self.should_process():
            return original_script

        prompt = self.prompt_factory.prompt(
            prompt_file="translation_prompt.yaml",
            prompt_key="translation",
            placeholders={
                "source_language": self.youtube_language.value,
                "script": original_script,
                "parsed_format": self.parser_format(
                    TranslatedSegment
                ),
            },
        )

        response = await self.provider.generate(prompt=prompt.template, parser=TranslatedSegment)

        return response

