import os
import re
from dataclasses import dataclass

import yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

DEFAULT_TRANSCRIPT_MODEL = "llama3.2:3b"

DEFAULT_VALIDATOR_MODEL = "llama3.2:3b"

YOUTUBE_URL_PATTERN = re.compile(r"^https?://(www\.|m\.)?(youtube\.com|youtu\.be)/")


class ConfigError(ValueError):
    pass


def _require_non_empty_string(value, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"'{field_name}' is required and must be a non-empty string.")
    return value.strip()


def _validate_youtube_url(value: str) -> str:
    value = (value or "").strip()

    if value and not YOUTUBE_URL_PATTERN.match(value):
        raise ConfigError(f"'youtube_url' is not a valid YouTube URL: {value!r}")

    return value


@dataclass
class ModelsConfig:
    transcript: str
    validator: str

    def __post_init__(self) -> None:
        self.transcript = _require_non_empty_string(
            self.transcript,
            "models.transcript",
        )
        self.validator = _require_non_empty_string(
            self.validator,
            "models.validator",
        )

    @classmethod
    def from_dict(cls, data: dict | None = None) -> "ModelsConfig":
        if data is None:
            data = {}

        if not isinstance(data, dict):
            raise ConfigError("'models' must be a mapping.")

        return cls(
            transcript=data.get("transcript"),
            validator=data.get("validator"),
        )

    def to_dict(self) -> dict:
        return {
            "transcript": self.transcript,
            "validator": self.validator,
        }


@dataclass
class NotesMakerConfig:
    youtube_url: str
    models: ModelsConfig
    source_path: str | None = None

    def __post_init__(self) -> None:
        self.youtube_url = _validate_youtube_url(self.youtube_url)

        if not isinstance(self.models, ModelsConfig):
            raise ConfigError("'models' must be a ModelsConfig instance.")

    @property
    def transcript_model(self) -> str:
        return self.models.transcript

    @property
    def validator_model(self) -> str:
        return self.models.validator

    @classmethod
    def from_dict(
        cls,
        data: dict | None = None,
        source_path: str | None = None,
    ) -> "NotesMakerConfig":
        if data is None:
            data = {}

        if not isinstance(data, dict):
            raise ConfigError("Config data must be a mapping.")

        return cls(
            youtube_url=data.get("youtube_url") or "",
            models=ModelsConfig.from_dict(data.get("models")),
            source_path=source_path,
        )

    def to_dict(self) -> dict:
        return {
            "youtube_url": self.youtube_url,
            "models": self.models.to_dict(),
        }


def _find_config(path: str | None) -> str | None:
    if path:
        return path

    if os.path.isfile(CONFIG_PATH):
        return CONFIG_PATH

    cwd_config = os.path.join(os.getcwd(), "config.yaml")

    if os.path.isfile(cwd_config):
        return cwd_config

    return None


def load_config(path: str | None = None) -> NotesMakerConfig:
    config_path = _find_config(path)

    if not config_path:
        return NotesMakerConfig(
            youtube_url="",
            models=ModelsConfig(
                transcript=DEFAULT_TRANSCRIPT_MODEL,
                validator=DEFAULT_VALIDATOR_MODEL,
            ),
        )

    with open(config_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if data is None:
        data = {}

    if not isinstance(data, dict):
        raise ConfigError(
            f"Config file {config_path} must contain a mapping at the top level."
        )

    return NotesMakerConfig.from_dict(data, source_path=config_path)
