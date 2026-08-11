from enum import Enum


class SupportedLanguage(str, Enum):
    ENGLISH = "english"
    HINDI = "hindi"
    BENGALI = "bengali"

    @classmethod
    def _missing_(cls, value):
        supported = ", ".join(f"'{language.value}'" for language in cls)

        raise ValueError(
            f"Unsupported language: '{value}'. "
            f"Supported languages are: {supported}"
        )