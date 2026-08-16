import yt_dlp

from utils.environment_system import EnvironmentSystem
from utils.string_constants import (
    AUDIO_OUTPUT_DIRECTORY,
    BEST_AUDIO_FORMAT,
    FFMPEG,
    FFMPEG_EXTRACT_AUDIO,
    ID,
    NODE,
    VIDEO_ID_FORMAT,
    WAV,
    WAV_FILE_EXTENSION,
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
