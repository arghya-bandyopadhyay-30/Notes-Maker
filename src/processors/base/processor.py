from abc import ABC

from langchain_core.output_parsers import PydanticOutputParser

from src.prompts.factory import PromptFactory
from src.utils.config import LLMConfig
from src.utils.environment import EnvironmentSystem
from src.utils.languages import SupportedLanguages


class Processor(ABC):
    def __init__(self, youtube_language: SupportedLanguages, llm: LLMConfig, prompt_factory: PromptFactory):
        self.youtube_language = youtube_language
        # environment_system.ensure_ollama_model(model)
        self.prompt_factory = prompt_factory
        self.parser_format = lambda parser: PydanticOutputParser(
            pydantic_object=parser
        ).get_format_instructions()
        self.provider = llm.provider

    def should_process(self) -> bool:
        return not (self.youtube_language == SupportedLanguages.ENGLISH)
