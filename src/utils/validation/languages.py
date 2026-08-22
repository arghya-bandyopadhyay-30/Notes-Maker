from enum import Enum


class SupportedLanguages(str, Enum):
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

    @property
    def language_code(self) -> str:
        return {
            SupportedLanguages.ENGLISH: "en",
            SupportedLanguages.HINDI: "hi",
            SupportedLanguages.BENGALI: "bn"
        }[self]
