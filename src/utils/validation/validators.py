from typing import Any

from src.utils.formatting.strings import (
    CONFIG_DATA_MUST_BE_A_DICT,
    FIELD_IS_NOT_A_DIRECTORY,
    FIELD_IS_REQUIRED,
    FIELD_MUST_BE_NON_EMPTY_STRING,
    MISSING_PLACEHOLDERS,
)
from src.utils.io.filesystem import FileSystem


def require_field(data: dict, field: str):
    if not isinstance(data, dict):
        raise TypeError(CONFIG_DATA_MUST_BE_A_DICT)

    if field not in data:
        raise KeyError(FIELD_IS_REQUIRED.format(field))

    return data[field]


def require_directory_path(
    path: str,
    field: str,
    file_system: FileSystem,
) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(FIELD_MUST_BE_NON_EMPTY_STRING.format(field))

    if file_system.path_exists(path) and not file_system.is_dir(path):
        raise NotADirectoryError(FIELD_IS_NOT_A_DIRECTORY.format(field, path))

    return path


def validate_parameters(parameters: list[str], placeholders: dict[str, Any]) -> None:
    required_parameters = set(parameters)
    provided_parameters = set(placeholders.keys())
    missing_placeholder = required_parameters - provided_parameters

    if missing_placeholder:
        raise ValueError(MISSING_PLACEHOLDERS.format(", ".join(missing_placeholder)))
