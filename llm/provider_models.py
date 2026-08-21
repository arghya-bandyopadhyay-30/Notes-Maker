from enum import Enum

class ProviderModels(Enum):
    OLLAMA = "ollama"
    OPEN_CODE = "open_code"

    @classmethod
    def _missing_(cls, value):
        supported = ", ".join(f"'{provider.value}'" for provider in cls)

        raise ValueError(
            f"Unsupported provider: '{value}'. "
            f"Supported providers are: {supported}"
        )
