from pathlib import Path

from .file_system import FileSystem


class AppConfig:
    def __init__(
        self,
        config_path: str = "config.yaml",
        file_system: FileSystem | None = None,
    ):
        self.config_path = Path(config_path)
        self.file_system = file_system or FileSystem()
        self.data: dict = {}
        self.youtube_url: str = ""
        self.models: dict = {
            "transcript": "",
            "validator": "",
        }

    def load(self) -> "AppConfig":
        self.data = self.file_system.read_yaml(self.config_path)

        self.youtube_url = self.data.get("youtube_url", "") or ""

        models = self.data.get("models") or {}

        self.models = {
            "transcript": (models.get("transcript") or "").strip(),
            "validator": (models.get("validator") or "").strip(),
        }

        return self
