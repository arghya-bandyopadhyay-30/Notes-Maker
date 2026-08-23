import importlib

from src.llm.base.llm_provider import LLMProvider
from src.transcribers.transcriber import Transcriber
from src.utils.config.dependency_container import DependencyContainer
from src.utils.formatting.strings import (
    LLM_MODULE_PATH,
    TRANSCRIBER_MODULE_PATH,
    PROVIDER_SUFFIX,
    TRANSCRIBER_SUFFIX,
)
from src.utils.naming.naming_case import snake_to_pascal_case


def get_llm_provider_class_name(provider_model_name: str, dependencies: DependencyContainer) -> LLMProvider:
    module = importlib.import_module(LLM_MODULE_PATH.format(provider_model_name))
    class_name = getattr(module, f"{snake_to_pascal_case(provider_model_name.capitalize())}{PROVIDER_SUFFIX}")

    return class_name(dependencies=dependencies)


def get_transcriber(language: str, url: str, dependencies: DependencyContainer) -> Transcriber:
    module = importlib.import_module(TRANSCRIBER_MODULE_PATH.format(language))
    class_name = getattr(module, f"{snake_to_pascal_case(language.capitalize())}{TRANSCRIBER_SUFFIX}")

    return class_name(
        url=url,
        dependencies=dependencies
    )