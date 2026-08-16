import importlib

from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem


def get_transcriber(language: str, url: str, environment_system: EnvironmentSystem) -> Transcriber:
    module = importlib.import_module(f"transcribers.{language}_transcriber")
    class_name = getattr(module, f"{language.capitalize()}Transcriber")

    return class_name(
        url=url,
        environment_system=environment_system
    )
