from .config import Config
from .dependency_container import DependencyContainer


class AppConfigService:
    def __init__(
        self,
        dependencies: DependencyContainer,
        config_path: str,
    ):
        self.dependencies = dependencies
        self.config_path = config_path

    def get_config(self) -> Config:
        data = self.dependencies.file_system.read_yaml(self.config_path)

        return Config.from_dict(data, dependencies=self.dependencies)