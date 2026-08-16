import yt_dlp

from utils.environment_system import EnvironmentSystem
from utils.string_constants import AUDIO_OUTPUT_DIRECTORY

def download_audio_as_mp3(url: str, environment_system: EnvironmentSystem) -> str:
    node_path = environment_system.find_executable("node")
    environment_system.find_executable("ffmpeg")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{AUDIO_OUTPUT_DIRECTORY}/%(id)s.%(ext)s",
        "js_runtimes": {
            "node": {
                "path": node_path,
            }
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
