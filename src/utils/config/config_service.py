from src.utils.config.config import AppConfig
from src.utils.config.container import DependencyContainer


class AppConfigService:
    def __init__(
        self,
        dependencies: DependencyContainer,
        config_path: str,
    ):
        self.dependencies = dependencies
        self.config_path = config_path

    def get_config(self) -> AppConfig:
        data = self.dependencies.file_system.read_yaml(self.config_path)

        return AppConfig.from_dict(data, dependencies=self.dependencies)