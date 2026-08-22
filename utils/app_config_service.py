from .config import Config
from .dependency_container import DependencyContainer
from pipeline_statistics.execution_time import execution_time


class AppConfigService:
    def __init__(
        self,
        dependencies: DependencyContainer,
        config_path: str,
    ):
        self.dependencies = dependencies
        self.config_path = config_path

    @execution_time
    def get_config(self) -> Config:
        data = self.dependencies.file_system.read_yaml(self.config_path)

        return Config.from_dict(data, dependencies=self.dependencies)