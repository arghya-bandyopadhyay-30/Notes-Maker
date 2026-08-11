from pathlib import Path

import yaml


class FileSystem:
    def path_exists(self, path: str | Path) -> bool:
        return Path(path).exists()

    def is_file(self, path: str | Path) -> bool:
        return Path(path).is_file()

    def read_yaml(self, path: str | Path) -> dict:
        path = Path(path)

        if not self.is_file(path):
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return data or {}
