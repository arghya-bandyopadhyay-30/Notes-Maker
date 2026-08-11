from dataclasses import dataclass

from .string_constants import MODELS, TRANSCRIPT, VALIDATOR, YOUTUBE_URL


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
        data = data or {}

        return cls(
            transcript=data.get(TRANSCRIPT, ""),
            validator=data.get(VALIDATOR, ""),
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
        data = data or {}

        return cls(
            youtube_url=data.get(YOUTUBE_URL, ""),
            models=ModelsConfig.from_dict(data.get(MODELS)),
        )
