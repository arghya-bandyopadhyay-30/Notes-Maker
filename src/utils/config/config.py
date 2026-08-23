from dataclasses import dataclass

from src.llm.llm_provider import LLMProvider
from src.llm.provider_models import ProviderModels
from src.transcribers.transcriber import Transcriber
from src.utils.validation.supported_languages import SupportedLanguages
from src.utils.config.dependency_container import DependencyContainer
from src.utils.naming.resolver import get_transcriber, get_llm_provider_class_name
from src.utils.formatting.strings import (
    LANGUAGE,
    LLM,
    MODELS,
    OUTPUT_DIRECTORY,
    PROVIDER_MODEL,
    TRANSLATOR,
    URL,
    VALIDATOR,
    YOUTUBE,
)
from src.utils.validation.validators import require_directory_path, require_field


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
            dependencies=dependencies
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
    provider_model: ProviderModels
    models: ModelsConfig
    provider: LLMProvider

    def to_dict(self) -> dict:
        return {
            PROVIDER_MODEL: self.provider_model.value,
            MODELS: self.models.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict, dependencies: DependencyContainer) -> "LLMConfig":
        provider_model_name = require_field(data, PROVIDER_MODEL)
        provider_model = ProviderModels(provider_model_name.lower())

        return cls(
            provider_model=provider_model,
            models=ModelsConfig.from_dict(require_field(data, MODELS)),
            provider=get_llm_provider_class_name(
                provider_model_name=provider_model.value,
                dependencies=dependencies
            )
        )


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
                data=require_field(data, YOUTUBE),
                dependencies=dependencies
            ),
            output_directory=require_directory_path(
                require_field(data, OUTPUT_DIRECTORY),
                OUTPUT_DIRECTORY,
                dependencies.file_system,
            ),
            llm=LLMConfig.from_dict(
                data=require_field(data, LLM),
                dependencies=dependencies
            ),
        )