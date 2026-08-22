from enum import Enum


class SupportedLanguages(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    BENGALI = "bn"

    @classmethod
    def _missing_(cls, value):
        supported = ", ".join(f"'{language.value}'" for language in cls)

        raise ValueError(
            f"Unsupported language: '{value}'. "
            f"Supported languages are: {supported}"
        )