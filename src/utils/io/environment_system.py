import shutil
import subprocess
import time
from contextlib import contextmanager

import ollama

from src.utils.formatting.strings import (
    EXECUTABLE_NOT_FOUND_ERROR,
    MODEL_ALREADY_EXISTS,
    MODEL_DOWNLOADED_SUCCESS,
    MODEL_NOT_FOUND_PULLING,
    OPERATION_TIME_FORMAT,
)


class EnvironmentSystem:
    def find_executable(self, executable: str) -> str:
        executable_path = shutil.which(executable)

        if executable_path is None:
            raise ValueError(EXECUTABLE_NOT_FOUND_ERROR.format(executable.capitalize()))

        return executable_path

    def start_subprocess(self, command: list[str]) -> subprocess.Popen[str]:
        return subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

    def timeout_subprocess(self) -> type[subprocess.TimeoutExpired]:
        return subprocess.TimeoutExpired

    def ensure_ollama_model(self, model_name: str):
        installed_models = {model.model for model in ollama.list().models}

        if model_name in installed_models:
            print(MODEL_ALREADY_EXISTS.format(model_name))
            return

        print(MODEL_NOT_FOUND_PULLING.format(model_name))

        ollama.pull(model_name)

        print(MODEL_DOWNLOADED_SUCCESS.format(model_name))

    @contextmanager
    def timed(self, operation: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            print(OPERATION_TIME_FORMAT.format(operation, elapsed))
