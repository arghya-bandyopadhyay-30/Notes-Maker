from dataclasses import dataclass

from transcribers.transcriber import Transcriber
from utils.supported_languages import SupportedLanguages
from llm.provider_models import ProviderModels

from .dependency_container import DependencyContainer
from .get_transcriber import get_transcriber
from .string_constants import (
    LANGUAGE,
    LLM,
    MODELS,
    OUTPUT_DIRECTORY,
    PROVIDER,
    TRANSLATOR,
    URL,
    VALIDATOR,
    YOUTUBE,
)
from .validation import require_directory_path, require_field


@dataclass
class YoutubeConfig:
    url: str
    language: SupportedLanguages
    transcriber: Transcriber

    def to_dict(self) -> dict:
        return {
            URL: self.url,
            LANGUAGE: self.language.value,
        }

    @classmethod
    def from_dict(cls, data: dict, dependencies: DependencyContainer) -> "YoutubeConfig":
        youtube_url = require_field(data, URL)
        language_code = require_field(data, LANGUAGE)
        language = SupportedLanguages(language_code.lower())
        transcriber = get_transcriber(
            language=language.value,
            url=youtube_url,
            environment_system=dependencies.environment_system
        )

        return cls(
            url=youtube_url,
            language=language,
            transcriber=transcriber
        )


@dataclass
class ModelsConfig:
    translator: str
    validator: str

    def to_dict(self) -> dict:
        return {
            TRANSLATOR: self.translator,
            VALIDATOR: self.validator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelsConfig":
        return cls(
            translator=require_field(data, TRANSLATOR),
            validator=require_field(data, VALIDATOR),
        )


@dataclass
class LLMConfig:
    provider: ProviderModels
    models: ModelsConfig

    def to_dict(self) -> dict:
        return {
            PROVIDER: self.provider.value,
            MODELS: self.models.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict, dependencies: DependencyContainer) -> "LLMConfig":
        provider_name = require_field(data, PROVIDER)
        provider = ProviderModels(provider_name.lower())

        return cls(
            provider=provider,
            models=ModelsConfig.from_dict(require_field(data, MODELS)),
        )


@dataclass
class Config:
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
    ) -> "Config":
        return cls(
            youtube=YoutubeConfig.from_dict(
                data=require_field(data, YOUTUBE),
                dependencies=dependencies
            ),
            output_directory=require_directory_path(
                require_field(data, OUTPUT_DIRECTORY),
                OUTPUT_DIRECTORY,
                dependencies,
            ),
            llm=LLMConfig.from_dict(
                data=require_field(data, LLM),
                dependencies=dependencies
            ),
        )