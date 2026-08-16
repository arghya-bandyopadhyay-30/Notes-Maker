from .environment_system import EnvironmentSystem
from .file_system import FileSystem


class DependencyContainer:
    def __init__(self):
        self.file_system = FileSystem()
        self.environment_system = EnvironmentSystem()
