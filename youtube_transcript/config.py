import os

import yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")

DEFAULT_MODELS = {
    "transcript": "llama3.2:3b",
    "validator": "llama3.2:3b",
}


def _find_config(path: str | None) -> str | None:
    if path:
        return path

    if os.path.isfile(CONFIG_PATH):
        return CONFIG_PATH

    cwd_config = os.path.join(os.getcwd(), "config.yaml")

    if os.path.isfile(cwd_config):
        return cwd_config

    return None


def load_config(path: str | None = None) -> dict:
    config = {
        "youtube_url": "",
        "models": dict(DEFAULT_MODELS),
    }

    config_path = _find_config(path)

    if not config_path:
        return config

    config["_path"] = config_path

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    except Exception as error:
        print(f"Warning: Could not read config {config_path}: {error}")
        return config

    if data.get("youtube_url"):
        config["youtube_url"] = str(data["youtube_url"]).strip()

    models = data.get("models") or {}

    if models.get("transcript"):
        config["models"]["transcript"] = str(models["transcript"]).strip()

    if models.get("validator"):
        config["models"]["validator"] = str(models["validator"]).strip()

    return config
