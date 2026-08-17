from typing import Any

from utils.file_system import FileSystem


class PromptFactory:
    def __init__(self, prompt_directory: str, file_system: FileSystem):
        self.prompt_directory = prompt_directory
        self.file_system = file_system

    def create(self, prompt_file: str, prompt_key: str, parameters: dict[str, Any]):
        pass