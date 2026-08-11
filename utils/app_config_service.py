from .config import Config
from .file_system import FileSystem


class AppConfigService:
    def __init__(
        self,
        file_system: FileSystem,
        config_path: str,
    ):
        self.file_system = file_system
        self.config_path = config_path

    def get_config(self) -> Config:
        data = self.file_system.read_yaml(self.config_path)

        return Config.from_dict(data, file_system=self.file_system)