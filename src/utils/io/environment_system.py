import shutil
import subprocess

from src.utils.formatting.strings import (
    EXECUTABLE_NOT_FOUND_ERROR,
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
