from dataclasses import dataclass

from .dependency_container import DependencyContainer
from .string_constants import (
    MODELS,
    OUTPUT_DIRECTORY,
    TRANSCRIPT,
    VALIDATOR,
    YOUTUBE_URL,
)
from .validation import _require_directory_path, _require_field


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
            transcript=_require_field(data, TRANSCRIPT),
            validator=_require_field(data, VALIDATOR),
        )


@dataclass
class Config:
    youtube_url: str
    output_directory: str
    models: ModelsConfig

    def to_dict(self) -> dict:
        return {
            YOUTUBE_URL: self.youtube_url,
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
            youtube_url=_require_field(data, YOUTUBE_URL),
            output_directory=_require_directory_path(
                _require_field(data, OUTPUT_DIRECTORY),
                OUTPUT_DIRECTORY,
                dependencies,
            ),
            models=ModelsConfig.from_dict(_require_field(data, MODELS)),
        )