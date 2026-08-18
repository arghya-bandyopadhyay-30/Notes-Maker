from typing import Any

from prompt_factory.prompt import Prompt
from utils.file_system import FileSystem
from utils.string_constants import PROMPT_RESOURCES_DIRECTORY, PROMPT_FACTORY_DIRECTORY


class PromptFactory:
    def __init__(self, file_system: FileSystem):
        self.file_system = file_system

    def create(self, prompt_file: str, prompt_key: str, placeholders: dict[str, Any]):
        prompt_file_path = self.file_system.join_paths(
            PROMPT_FACTORY_DIRECTORY,
            PROMPT_RESOURCES_DIRECTORY,
            prompt_file,
        )
        prompts = self.file_system.read_yaml(prompt_file_path)

        if prompt_key not in prompts:
            raise KeyError(f"Prompt '{prompt_key}' not found in '{prompt_file}'")

        prompt = Prompt.from_dict(
            data=prompts[prompt_key],
            placeholders=placeholders
        )
        print(prompt)
