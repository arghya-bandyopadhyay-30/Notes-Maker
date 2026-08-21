import importlib

from llm.llm_provider import LLMProvider
from utils.snake_to_pascal_case import snake_to_pascal_case


def get_provider(provider: str) -> LLMProvider:
    module = importlib.import_module(f"llm.{provider}_provider")
    class_name = getattr(module, f"{snake_to_pascal_case(provider.capitalize())}Provider")

    return class_name()
