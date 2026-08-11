from .file_system import FileSystem


class DependencyContainer:
    def __init__(
        self,
        file_system: FileSystem,
    ):
        self.file_system = file_system