import shutil


class EnvironmentSystem:
    def find_executable(self, executable: str) -> str:
        executable_path = shutil.which(executable)

        if executable_path is None:
            raise RuntimeError(f"{executable.capitalize()} was not found in PATH")

        return executable_path