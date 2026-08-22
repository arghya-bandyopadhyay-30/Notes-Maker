from abc import ABC

from langchain_core.output_parsers import PydanticOutputParser

from prompt_factory.prompt_factory import PromptFactory
from utils.config import LLMConfig
from utils.environment_system import EnvironmentSystem
from utils.supported_languages import SupportedLanguages


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
