from .dependency_container import DependencyContainer
from .string_constants import (
    CONFIG_DATA_MUST_BE_A_DICT,
    FIELD_IS_NOT_A_DIRECTORY,
    FIELD_IS_REQUIRED,
    FIELD_MUST_BE_NON_EMPTY_STRING,
)


def require_field(data: dict, field: str):
    if not isinstance(data, dict):
        raise TypeError(CONFIG_DATA_MUST_BE_A_DICT)

    if field not in data:
        raise KeyError(FIELD_IS_REQUIRED.format(field))

    return data[field]


def require_directory_path(
    path: str,
    field: str,
    dependencies: DependencyContainer,
) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(FIELD_MUST_BE_NON_EMPTY_STRING.format(field))

    file_system = dependencies.file_system

    if file_system.path_exists(path) and not file_system.is_dir(path):
        raise NotADirectoryError(FIELD_IS_NOT_A_DIRECTORY.format(field, path))

    return path