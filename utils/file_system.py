from pathlib import Path

import yaml


class FileSystem:
    def path_exists(self, path: str) -> bool:
        return Path(path).exists()

    def is_file(self, path: str) -> bool:
        return Path(path).is_file()

    def read_yaml(self, path: str) -> dict:
        path = Path(path)

        if not self.is_file(path):
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if data is None:
            raise ValueError(f"YAML file is empty: {path}")

        if not isinstance(data, dict):
            raise ValueError(
                f"YAML file must contain a mapping at the top level: {path}"
            )

        return data

    def ensure_directory_exists(self, path: str) -> str:
        path_obj = Path(path)

        if path_obj.exists() and not path_obj.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {path}")

        path_obj.mkdir(parents=True, exist_ok=True)

        return str(path_obj)
