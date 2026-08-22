from src.utils.io.environment import EnvironmentSystem
from src.utils.io.filesystem_ops import FileSystem


class DependencyContainer:
    def __init__(self):
        self.file_system = FileSystem()
        self.environment_system = EnvironmentSystem()
        from src.prompts.factory import PromptFactory
        self.prompt_factory = PromptFactory(
            file_system=self.file_system
        )
