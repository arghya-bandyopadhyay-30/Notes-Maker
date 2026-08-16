import importlib

from transcribers.transcriber import Transcriber


def get_transcriber(language: str) -> Transcriber:
    module = importlib.import_module(f"transcribers.{language}_transcriber")
    class_name = getattr(module, f"{language.capitalize()}Transcriber")

    return class_name()
