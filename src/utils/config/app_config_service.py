from src.bootstrap.container import DependencyContainer
from src.utils.config.app_config import AppConfig


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
