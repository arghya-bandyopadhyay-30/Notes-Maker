from langchain_core.output_parsers import PydanticOutputParser

from src.pipeline.statistics.execution import execution_time
from src.processors.models import TranslatedSegment, TranslationValidation
from src.processors.script import ProcessedScript
from src.prompts.factory import PromptFactory
from src.utils.config.config import LLMConfig
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
            f"Translating the {self.youtube_language.value.capitalize()} script to English translated script..."
        )
        prompt = self.prompt_factory.prompt(
            prompt_file="translation.yaml",
            prompt_key="translation",
            placeholders={
                "source_language": self.youtube_language.value,
                "script": original_script,
                "parsed_format": self.parser_format(
                    TranslatedSegment
                ),
            },
        )

        response: TranslatedSegment = await self.provider.generate(prompt=prompt.template, parser=TranslatedSegment)

        return response.text


    @execution_time
    async def validate(self, original_script: str, translated_script: str) -> TranslationValidation:
        print(
            f"Validating the {self.youtube_language.value.capitalize()} script to English translated script..."
        )
        prompt = self.prompt_factory.prompt(
            prompt_file="validation.yaml",
            prompt_key="validation",
            placeholders={
                "source_language": self.youtube_language.value,
                "original_script": original_script,
                "translated_script": translated_script,
                "parsed_format": self.parser_format(
                    TranslationValidation
                ),
            },
        )

        response: TranslationValidation = await self.provider.generate(prompt=prompt.template, parser=TranslationValidation)

        return response

    @execution_time
    async def process(self, original_script: str) -> ProcessedScript:
        if not self.should_process():
            return ProcessedScript(script=original_script, validation_score=1.0)

        translated_script = await self.translate(original_script)
        validation = await self.validate(
            original_script=original_script,
            translated_script=translated_script
        )

        return ProcessedScript(
            script=translated_script if validation.is_valid else original_script,
            validation_score=validation.validation_score,
            missing_information=validation.missing_information,
            incorrect_meaning=validation.incorrect_meaning,
            hallucinated_information=validation.hallucinated_information,
            incorrect_terminology=validation.incorrect_terminology,
            major_grammatical_errors=validation.major_grammatical_errors,
        )
