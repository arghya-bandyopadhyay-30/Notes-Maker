from .dependency_container import DependencyContainer


def _require_field(data: dict, field: str):
    if not isinstance(data, dict):
        raise TypeError("config data must be a dict")

    if field not in data:
        raise KeyError(f"'{field}' is required")

    return data[field]


def _require_directory_path(
    path: str,
    field: str,
    dependencies: DependencyContainer,
) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError(f"'{field}' must be a non-empty string")

    file_system = dependencies.file_system

    if file_system.path_exists(path) and not file_system.is_dir(path):
        raise NotADirectoryError(f"'{field}' is not a directory: {path}")

    return path