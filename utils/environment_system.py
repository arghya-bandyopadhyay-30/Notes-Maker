import shutil
import subprocess
import time
from contextlib import contextmanager

import ollama


class EnvironmentSystem:
    def find_executable(self, executable: str) -> str:
        executable_path = shutil.which(executable)

        if executable_path is None:
            raise ValueError(f"{executable.capitalize()} was not found in PATH")

        return executable_path

    def start_process(self, command: list[str]) -> subprocess.Popen[str]:
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

    def ensure_ollama_model(self, model_name: str):
        installed_models = {
            model.model
            for model in ollama.list().models
        }

        if model_name in installed_models:
            print(
                f"Model '{model_name}' already exists. Skipping pull."
            )
            return

        print(f"Model '{model_name}' not found. Pulling model...")

        ollama.pull(model_name)

        print(f"Model '{model_name}' downloaded successfully.")

    @contextmanager
    def timed(self, operation: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            print(f"{operation} took {elapsed:.3f}s")
