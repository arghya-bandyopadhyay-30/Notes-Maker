import importlib

from src.llm.base import LLMProvider
from src.transcribers.base import Transcriber
from src.utils.environment import EnvironmentSystem
from src.utils.naming_case import snake_to_pascal_case


def get_llm_provider_class_name(provider_model_name: str, environment_system: EnvironmentSystem) -> LLMProvider:
    module = importlib.import_module(f"llm.{provider_model_name}_provider")
    class_name = getattr(module, f"{snake_to_pascal_case(provider_model_name.capitalize())}Provider")

    return class_name(environment_system=environment_system)

def get_transcriber(language: str, url: str, environment_system: EnvironmentSystem) -> Transcriber:
    module = importlib.import_module(f"transcribers.{language}_transcriber")
    class_name = getattr(module, f"{snake_to_pascal_case(language.capitalize())}Transcriber")

    return class_name(
        url=url,
        environment_system=environment_system
    )