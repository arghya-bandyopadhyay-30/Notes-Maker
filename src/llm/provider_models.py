from enum import Enum

from src.utils.formatting.strings import (
    PROVIDER_OLLAMA,
    PROVIDER_OPEN_CODE,
    UNSUPPORTED_PROVIDER_ERROR,
)


class ProviderModels(Enum):
    OLLAMA = PROVIDER_OLLAMA
    OPEN_CODE = PROVIDER_OPEN_CODE

    @classmethod
    def _missing_(cls, value):
        supported = ", ".join(f"'{provider.value}'" for provider in cls)

        raise ValueError(UNSUPPORTED_PROVIDER_ERROR.format(value, supported))
