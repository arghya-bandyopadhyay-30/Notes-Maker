from langchain_core.output_parsers import PydanticOutputParser

from src.processors.models import TranslatedSegment
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

    async def translate(self, original_script: str) -> str:
        if not self.should_process():
            return original_script

        print(
            f"Translating the {self.youtube_language.value.capitalize()} script to English translated scrip..."
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
    
    async def validate(self, original_script: str, translated_script: str) -> float:
        if not self.should_process():
            return 1

        print(
            f"Validating the {self.youtube_language.value.capitalize()} script to English translated scrip..."
        )
        # prompt = self.prompt_factory.prompt(
        #     prompt_file="validation.yaml",
        #     prompt_key="validation",
        #     placeholders={
        #         "source_language": self.youtube_language.value,
        #         "original_script": original_script,
        #         "translated_script": translated_script,
        #         "parsed_format": self.parser_format(
        #             TranslationValidation
        #         ),
        #     },
        # )
        #
        # response = await self.provider.generate(prompt=prompt.template, parser=TranslationValidation)
        # print("="*80)
        # print(response)
        # print("="*80)

        return 0

    async def process(self, original_script: str) -> tuple[str, float]:
        translated_script = await self.translate(original_script)
        validation_score = await self.validate(
            original_script=original_script,
            translated_script=translated_script
        )
        return translated_script, validation_score
