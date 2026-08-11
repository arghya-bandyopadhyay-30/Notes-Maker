from dataclasses import dataclass


@dataclass
class ModelsConfig:
    transcript: str
    validator: str

    def to_dict(self) -> dict:
        return {
            "transcript": self.transcript,
            "validator": self.validator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelsConfig":
        data = data or {}

        return cls(
            transcript=data.get("transcript", ""),
            validator=data.get("validator", ""),
        )


@dataclass
class Config:
    youtube_url: str
    models: ModelsConfig

    def to_dict(self) -> dict:
        return {
            "youtube_url": self.youtube_url,
            "models": self.models.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        data = data or {}

        return cls(
            youtube_url=data.get("youtube_url", ""),
            models=ModelsConfig.from_dict(data.get("models")),
        )
