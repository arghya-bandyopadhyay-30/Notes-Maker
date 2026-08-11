from dataclasses import dataclass

from .string_constants import MODELS, TRANSCRIPT, VALIDATOR, YOUTUBE_URL


def _require_non_empty_string(value, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{field}' must be a non-empty string")

    return value.strip()


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
        if not isinstance(data, dict):
            raise TypeError("'models' config must be a dict")

        return cls(
            transcript=_require_non_empty_string(data[TRANSCRIPT], TRANSCRIPT),
            validator=_require_non_empty_string(data[VALIDATOR], VALIDATOR),
        )


@dataclass
class Config:
    youtube_url: str
    models: ModelsConfig

    def to_dict(self) -> dict:
        return {
            YOUTUBE_URL: self.youtube_url,
            MODELS: self.models.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        if not isinstance(data, dict):
            raise TypeError("config must be a dict")

        return cls(
            youtube_url=_require_non_empty_string(data[YOUTUBE_URL], YOUTUBE_URL),
            models=ModelsConfig.from_dict(data[MODELS]),
        )
