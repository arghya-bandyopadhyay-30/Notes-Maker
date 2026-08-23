from dataclasses import dataclass

from src.llm.base.llm_provider import LLMProvider
from src.llm.provider_models import ProviderModels
from src.utils.config.models_config import ModelsConfig
from src.bootstrap.container import DependencyContainer
from src.utils.naming.resolver import get_llm_provider_class_name
from src.utils.formatting.strings import (
    MODELS_CONFIG,
    PROVIDER_MODEL,
    VALIDATION_THRESHOLD,
    VALIDATION_THRESHOLD_KEY,
)
from src.utils.validation.validators import require_field


@dataclass
class LLMConfig:
    provider_model: ProviderModels
    models_config: ModelsConfig
    provider: LLMProvider
    validation_threshold: float = VALIDATION_THRESHOLD

    def to_dict(self) -> dict:
        return {
            PROVIDER_MODEL: self.provider_model.value,
            MODELS_CONFIG: self.models_config.to_dict(),
            VALIDATION_THRESHOLD_KEY: self.validation_threshold,
        }

    @classmethod
    def from_dict(cls, data: dict, dependencies: DependencyContainer) -> "LLMConfig":
        provider_model_name = require_field(data, PROVIDER_MODEL)
        provider_model = ProviderModels(provider_model_name.lower())
        validation_threshold = data.get(VALIDATION_THRESHOLD_KEY, VALIDATION_THRESHOLD)

        return cls(
            provider_model=provider_model,
            models_config=ModelsConfig.from_dict(require_field(data, MODELS_CONFIG)),
            provider=get_llm_provider_class_name(
                provider_model_name=provider_model.value,
                dependencies=dependencies
            ),
            validation_threshold=validation_threshold,
        )