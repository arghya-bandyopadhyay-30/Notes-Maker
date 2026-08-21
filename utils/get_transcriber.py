import importlib

from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem
from utils.snake_to_pascal_case import snake_to_pascal_case


def get_transcriber(language: str, url: str, environment_system: EnvironmentSystem) -> Transcriber:
    module = importlib.import_module(f"transcribers.{language}_transcriber")
    class_name = getattr(module, f"{snake_to_pascal_case(language.capitalize())}Transcriber")

    return class_name(
        url=url,
        environment_system=environment_system
    )
