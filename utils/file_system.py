import os

import yaml


class FileSystem:
    def path_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def read_yaml(self, path: str) -> dict:
        if not self.is_file(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if data is None:
            raise ValueError(f"YAML file is empty: {path}")

        if not isinstance(data, dict):
            raise ValueError(
                f"YAML file must contain a mapping at the top level: {path}"
            )

        return data

    def ensure_directory_exists(self, path: str) -> str:
        if self.path_exists(path) and not self.is_dir(path):
            raise NotADirectoryError(f"Path is not a directory: {path}")

        os.makedirs(path, exist_ok=True)

        return path
