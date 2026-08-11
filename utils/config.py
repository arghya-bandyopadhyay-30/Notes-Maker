from dataclasses import dataclass

from .dependency_container import DependencyContainer
from .string_constants import (
    LANGUAGE,
    MODELS,
    OUTPUT_DIRECTORY,
    TRANSCRIPT,
    URL,
    VALIDATOR,
    YOUTUBE,
)
from .validation import require_directory_path, require_field


@dataclass
class YoutubeConfig:
    url: str
    language: str

    def to_dict(self) -> dict:
        return {
            URL: self.url,
            LANGUAGE: self.language,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "YoutubeConfig":
        return cls(
            url=require_field(data, URL),
            language=require_field(data, LANGUAGE),
        )


@dataclass
class ModelsConfig:
    transcript: str
    validator: str

    def to_dict(self) -> dict:
        return {
            TRANSCRIPT: self.transcript,
            VALIDATOR: self.validator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelsConfig":
        return cls(
            transcript=require_field(data, TRANSCRIPT),
            validator=require_field(data, VALIDATOR),
        )


@dataclass
class Config:
    youtube: YoutubeConfig
    output_directory: str
    models: ModelsConfig

    def to_dict(self) -> dict:
        return {
            YOUTUBE: self.youtube.to_dict(),
            OUTPUT_DIRECTORY: self.output_directory,
            MODELS: self.models.to_dict(),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        dependencies: DependencyContainer,
    ) -> "Config":
        return cls(
            youtube=YoutubeConfig.from_dict(require_field(data, YOUTUBE)),
            output_directory=require_directory_path(
                require_field(data, OUTPUT_DIRECTORY),
                OUTPUT_DIRECTORY,
                dependencies,
            ),
            models=ModelsConfig.from_dict(require_field(data, MODELS)),
        )
