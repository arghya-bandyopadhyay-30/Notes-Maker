import os

import yt_dlp
import yaml

from src.utils.io.environment import EnvironmentSystem
from src.utils.formatting.strings import (
    AUDIO_OUTPUT_DIRECTORY,
    BEST_AUDIO_FORMAT,
    FILE_NOT_FOUND,
    FFMPEG,
    FFMPEG_EXTRACT_AUDIO,
    ID,
    NODE,
    READ_MODE,
    UTF_8_ENCODING,
    VIDEO_ID_FORMAT,
    WAV,
    WAV_FILE_EXTENSION,
    WRITE_MODE,
    YAML_FILE_IS_EMPTY,
    YAML_FILE_MUST_BE_MAPPING,
)


def download_audio_as_wav(
    url: str,
    environment_system: EnvironmentSystem,
) -> str:
    node_path = environment_system.find_executable(NODE)
    environment_system.find_executable(FFMPEG)

    ydl_opts = {
        "format": BEST_AUDIO_FORMAT,
        "outtmpl": f"{AUDIO_OUTPUT_DIRECTORY}/{VIDEO_ID_FORMAT}.%(ext)s",
        "js_runtimes": {
            NODE: {
                "path": node_path,
            }
        },
        "remote_components": {"ejs:github",},
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "web_embedded",
                ],
            },
        },
        "postprocessors": [
            {
                "key": FFMPEG_EXTRACT_AUDIO,
                "preferredcodec": WAV,
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            url,
            download=True,
        )

    video_id = info[ID]

    return f"{AUDIO_OUTPUT_DIRECTORY}/{video_id}{WAV_FILE_EXTENSION}"


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
