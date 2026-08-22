from src.utils.environment import EnvironmentSystem
from src.utils.filesystem_ops import FileSystem


class DependencyContainer:
    def __init__(self):
        self.file_system = FileSystem()
        self.environment_system = EnvironmentSystem()
