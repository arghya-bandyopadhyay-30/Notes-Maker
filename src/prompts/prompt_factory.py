from typing import Any

from src.prompts.prompt import Prompt
from src.utils.io.filesystem import FileSystem
from src.utils.formatting.strings import (
    PROMPT_RESOURCES_DIRECTORY,
    PROMPT_FACTORY_DIRECTORY,
    PYDANTIC_VALIDATION_PROMPT_FILE,
    PYDANTIC_VALIDATION_PROMPT_KEY,
    PROMPT_NOT_FOUND_ERROR,
    PYDANTIC_VALIDATION_NOT_FOUND_ERROR,
)


class PromptFactory:
    def __init__(self, file_system: FileSystem):
        self.file_system = file_system

    def prompt(self, prompt_file: str, prompt_key: str, placeholders: dict[str, Any]) -> Prompt:
        prompt_file_path = self.file_system.join_paths(
            PROMPT_FACTORY_DIRECTORY,
            PROMPT_RESOURCES_DIRECTORY,
            prompt_file,
        )
        prompts = self.file_system.read_yaml(prompt_file_path)

        if prompt_key not in prompts:
            raise KeyError(PROMPT_NOT_FOUND_ERROR.format(prompt_key, prompt_file))

        return Prompt.from_dict(
            data=prompts[prompt_key],
            placeholders=placeholders
        )

    def pydantic_validation_prompt(self, placeholders: dict[str, Any]) -> Prompt:
        prompt_file_path = self.file_system.join_paths(
            PROMPT_FACTORY_DIRECTORY,
            PROMPT_RESOURCES_DIRECTORY,
            PYDANTIC_VALIDATION_PROMPT_FILE
        )
        prompts = self.file_system.read_yaml(prompt_file_path)

        if PYDANTIC_VALIDATION_PROMPT_KEY not in prompts:
            raise KeyError(PYDANTIC_VALIDATION_NOT_FOUND_ERROR)

        return Prompt.from_dict(
            data=prompts[PYDANTIC_VALIDATION_PROMPT_KEY],
            placeholders=placeholders
        )
