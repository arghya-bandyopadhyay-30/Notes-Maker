import os
from dataclasses import dataclass

from .string_constants import (
    MODELS,
    OUTPUT_DIRECTORY,
    TRANSCRIPT,
    VALIDATOR,
    YOUTUBE_URL,
)


def _require_field(data: dict, field: str):
    if not isinstance(data, dict):
        raise TypeError("config data must be a dict")

    if field not in data:
        raise KeyError(f"'{field}' is required")

    return data[field]


def _require_directory_path(path: str, field: str) -> str:
    if os.path.exists(path) and not os.path.isdir(path):
        raise NotADirectoryError(f"'{field}' is not a directory: {path}")

    return path


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

    def __post_init__(self) -> None:
        self.output_directory = _require_directory_path(
            self.output_directory,
            OUTPUT_DIRECTORY,
        )

    def to_dict(self) -> dict:
        return {
            YOUTUBE_URL: self.youtube_url,
            OUTPUT_DIRECTORY: self.output_directory,
            MODELS: self.models.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        return cls(
            youtube_url=_require_field(data, YOUTUBE_URL),
            output_directory=_require_field(data, OUTPUT_DIRECTORY),
            models=ModelsConfig.from_dict(_require_field(data, MODELS)),
        )
