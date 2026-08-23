import os

import yaml

from src.utils.formatting.strings import (
    FILE_NOT_FOUND,
    READ_MODE,
    UTF_8_ENCODING,
    YAML_FILE_IS_EMPTY,
    YAML_FILE_MUST_BE_MAPPING, WRITE_MODE,
)


class FileSystem:
    def path_exists(self, path: str) -> bool:
        return os.path.exists(path)

    def is_file(self, path: str) -> bool:
        return os.path.isfile(path)

    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def join_paths(self, primary_path: str, *paths: str) -> str:
        return os.path.join(primary_path, *paths)

    def read_yaml(self, path: str) -> dict:
        if not self.is_file(path):
            raise FileNotFoundError(FILE_NOT_FOUND.format(path))

        with open(path, READ_MODE, encoding=UTF_8_ENCODING) as file:
            data = yaml.safe_load(file)

        if data is None:
            raise ValueError(YAML_FILE_IS_EMPTY.format(path))

        if not isinstance(data, dict):
            raise ValueError(
                YAML_FILE_MUST_BE_MAPPING.format(path)
            )

        return data

    def write_yaml(self, path: str, content: dict) -> str:
        with open(path, WRITE_MODE, encoding=UTF_8_ENCODING) as file:
            yaml.safe_dump(content, file, sort_keys=False)

        return path

    def make_dirs(self, path: str) -> str:
        os.makedirs(path, exist_ok=True)
        return path

    def write_file(self, path: str, content: str) -> str:
        with open(path, WRITE_MODE, encoding=UTF_8_ENCODING) as file:
            file.write(content)

        return path

    def remove(self, path: str) -> None:
        try:
            os.remove(path)
        except FileNotFoundError:
            return
