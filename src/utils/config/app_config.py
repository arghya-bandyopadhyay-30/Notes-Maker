from dataclasses import dataclass

from src.bootstrap.container import DependencyContainer
from src.utils.config.llm_config import LLMConfig
from src.utils.config.youtube_config import YoutubeConfig
from src.utils.formatting.strings import (
    LLM,
    OUTPUT_DIRECTORY,
    YOUTUBE,
)
from src.utils.validation.validators import require_directory_path, require_field


@dataclass
class AppConfig:
    youtube: YoutubeConfig
    output_directory: str
    llm: LLMConfig

    def to_dict(self) -> dict:
        return {
            YOUTUBE: self.youtube.to_dict(),
            OUTPUT_DIRECTORY: self.output_directory,
            LLM: self.llm.to_dict(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        dependencies: DependencyContainer,
    ) -> "AppConfig":
        return cls(
            youtube=YoutubeConfig.from_dict(
                data=require_field(data, YOUTUBE), dependencies=dependencies
            ),
            output_directory=require_directory_path(
                require_field(data, OUTPUT_DIRECTORY),
                OUTPUT_DIRECTORY,
                dependencies.file_system,
            ),
            llm=LLMConfig.from_dict(data=require_field(data, LLM), dependencies=dependencies),
        )
