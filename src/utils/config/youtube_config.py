from dataclasses import dataclass

from src.transcribers.transcriber import Transcriber
from src.utils.validation.supported_languages import SupportedLanguages
from src.utils.config.dependency_container import DependencyContainer
from src.utils.naming.resolver import get_transcriber
from src.utils.formatting.strings import (
    LANGUAGE,
    URL,
)
from src.utils.validation.validators import require_field


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