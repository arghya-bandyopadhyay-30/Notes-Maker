import importlib

from src.llm.base import LLMProvider
from src.transcribers.base import Transcriber
from src.utils.config.container import DependencyContainer
from src.utils.io.environment import EnvironmentSystem
from src.utils.naming.naming_case import snake_to_pascal_case


def get_llm_provider_class_name(provider_model_name: str, dependencies: DependencyContainer) -> LLMProvider:
    module = importlib.import_module(f"src.llm.{provider_model_name}")
    class_name = getattr(module, f"{snake_to_pascal_case(provider_model_name.capitalize())}Provider")

    return class_name(dependencies=dependencies)


def get_transcriber(language: str, url: str, dependencies: DependencyContainer) -> Transcriber:
    module = importlib.import_module(f"src.transcribers.languages.{language}")
    class_name = getattr(module, f"{snake_to_pascal_case(language.capitalize())}Transcriber")

    return class_name(
        url=url,
        dependencies=dependencies
    )