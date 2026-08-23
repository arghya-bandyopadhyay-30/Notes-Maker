from langchain_core.output_parsers import PydanticOutputParser

from src.pipeline.statistics.execution import execution_time
from src.processors.models import TranslatedSegment, TranslationValidation
from src.processors.script import ProcessedScript
from src.prompts.factory import PromptFactory
from src.utils.config.config import LLMConfig
from src.utils.formatting.strings import (
    TRANSLATION_PROMPT_FILE,
    TRANSLATION_PROMPT_KEY,
    VALIDATION_PROMPT_FILE,
    VALIDATION_PROMPT_KEY,
    SOURCE_LANGUAGE_KEY,
    SCRIPT_KEY,
    PARSED_FORMAT_KEY,
    ORIGINAL_SCRIPT_KEY,
    TRANSLATED_SCRIPT_KEY,
    TRANSLATING_MESSAGE,
    VALIDATING_MESSAGE,
)
from src.utils.validation.languages import SupportedLanguages


class Processor:
    def __init__(self, youtube_language: SupportedLanguages, llm: LLMConfig, prompt_factory: PromptFactory):
        self.youtube_language = youtube_language
        self.prompt_factory = prompt_factory
        self.parser_format = lambda parser: PydanticOutputParser(
            pydantic_object=parser
        ).get_format_instructions()
        self.provider = llm.provider

    def should_process(self) -> bool:
        return not (self.youtube_language == SupportedLanguages.ENGLISH)

    @execution_time
    async def translate(self, original_script: str) -> str:
        print(
            TRANSLATING_MESSAGE.format(self.youtube_language.value.capitalize())
        )
        prompt = self.prompt_factory.prompt(
            prompt_file=TRANSLATION_PROMPT_FILE,
            prompt_key=TRANSLATION_PROMPT_KEY,
            placeholders={
                SOURCE_LANGUAGE_KEY: self.youtube_language.value,
                SCRIPT_KEY: original_script,
                PARSED_FORMAT_KEY: self.parser_format(
                    TranslatedSegment
                ),
            },
        )

        response: TranslatedSegment = await self.provider.generate(prompt=prompt.template, parser=TranslatedSegment)

        return response.text


    @execution_time
    async def validate(self, original_script: str, translated_script: str) -> TranslationValidation:
        if not self.should_process():
            return TranslationValidation(accuracy_score=1.0)

        print(
            VALIDATING_MESSAGE.format(self.youtube_language.value.capitalize())
        )
        prompt = self.prompt_factory.prompt(
            prompt_file=VALIDATION_PROMPT_FILE,
            prompt_key=VALIDATION_PROMPT_KEY,
            placeholders={
                SOURCE_LANGUAGE_KEY: self.youtube_language.value,
                ORIGINAL_SCRIPT_KEY: original_script,
                TRANSLATED_SCRIPT_KEY: translated_script,
                PARSED_FORMAT_KEY: self.parser_format(
                    TranslationValidation
                ),
            },
        )

        response: TranslationValidation = await self.provider.generate(prompt=prompt.template, parser=TranslationValidation)

        return response

    @execution_time
    async def process(self, original_script: str) -> ProcessedScript:
        if not self.should_process():
            return ProcessedScript(original_script=original_script, translated_script=original_script, validation_score=1.0)

        translated_script = await self.translate(original_script)
        validation = await self.validate(
            original_script=original_script,
            translated_script=translated_script
        )

        return ProcessedScript.from_dict({
            ORIGINAL_SCRIPT_KEY: original_script,
            TRANSLATED_SCRIPT_KEY: translated_script,
            **validation.__dict__
        })
