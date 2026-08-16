import importlib

from transcribers.transcriber import Transcriber


def get_transcriber(language: str, audio_path: str) -> Transcriber:
    module = importlib.import_module(f"transcribers.{language}_transcriber")
    class_name = getattr(module, f"{language.capitalize()}Transcriber")

    return class_name(audio_path=audio_path)
