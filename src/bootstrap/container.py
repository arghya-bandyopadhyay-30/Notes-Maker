from src.prompts.prompt_factory import PromptFactory
from src.utils.io.environment_system import EnvironmentSystem
from src.utils.io.filesystem import FileSystem


class DependencyContainer:
    def __init__(self) -> None:
        self.file_system = FileSystem()
        self.environment_system = EnvironmentSystem()
        self.prompt_factory = PromptFactory(file_system=self.file_system)
