from enum import Enum

from src.utils.formatting.strings import (
    LANG_ENGLISH,
    LANG_HINDI,
    LANG_BENGALI,
    LANG_CODE_EN,
    LANG_CODE_HI,
    LANG_CODE_BN,
    UNSUPPORTED_LANGUAGE_ERROR,
)


class SupportedLanguages(str, Enum):
    ENGLISH = LANG_ENGLISH
    HINDI = LANG_HINDI
    BENGALI = LANG_BENGALI

    @classmethod
    def _missing_(cls, value):
        supported = ", ".join(f"'{language.value}'" for language in cls)

        raise ValueError(
            UNSUPPORTED_LANGUAGE_ERROR.format(value, supported)
        )

    @property
    def language_code(self) -> str:
        return {
            SupportedLanguages.ENGLISH: LANG_CODE_EN,
            SupportedLanguages.HINDI: LANG_CODE_HI,
            SupportedLanguages.BENGALI: LANG_CODE_BN
        }[self]
