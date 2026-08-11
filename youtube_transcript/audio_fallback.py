import logging
import os
import shutil
import tempfile

import yt_dlp
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

WHISPER_MODEL = "small"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE_TYPE = "int8"

_whisper_model = None


def get_whisper_model() -> WhisperModel:
    global _whisper_model

    if _whisper_model is None:
        print(f"\nLoading Whisper model: {WHISPER_MODEL}")
        print("The first run may download the model.")

        _whisper_model = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )

        print("Whisper model loaded.")

    return _whisper_model


def _find_cookies_file() -> str | None:
    candidates = [
        os.path.join(os.path.dirname(__file__), "cookies.txt"),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "cookies.txt"),
        os.path.join(os.getcwd(), "cookies.txt"),
    ]

    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate

    return None


def download_audio(
    url: str,
    output_dir: str,
) -> str:
    output_template = os.path.join(
        output_dir,
        "youtube_audio.%(ext)s",
    )

    base_options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        "socket_timeout": 30,
        "retries": 3,
        "fragment_retries": 3,
    }

    if shutil.which("ffmpeg"):
        base_options["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ]

    print("\nDownloading YouTube audio...")

    cookies_file = _find_cookies_file()

    cookie_variants = []

    if cookies_file:
        cookie_variants.append({"cookiefile": cookies_file})
    else:
        cookie_variants.append({"cookiesfrombrowser": ("edge",)})
        cookie_variants.append({"cookiesfrombrowser": ("chrome",)})

    cookie_variants.append({})

    client_variants = [
        (None, "default"),
        (["android"], "android"),
        (["web_safari"], "web_safari"),
        (["ios"], "ios"),
    ]

    attempts = []

    for client_list, client_name in client_variants:
        for cookie in cookie_variants:
            options = dict(base_options)
            options.update(cookie)

            if client_list is not None:
                options["extractor_args"] = {
                    "youtube": {
                        "player_client": client_list,
                    }
                }

            attempts.append((options, client_name))

    last_error = None

    for options, client_name in attempts:
        print(f"Attempting download (player client: {client_name})...")

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.extract_info(
                    url,
                    download=True,
                )

            possible_files = [
                os.path.join(
                    output_dir,
                    filename,
                )
                for filename in os.listdir(output_dir)
            ]

            media_files = [
                path
                for path in possible_files
                if os.path.isfile(path)
                and not path.lower().endswith(".part")
                and path.lower().endswith(
                    (
                        ".wav",
                        ".mp3",
                        ".m4a",
                        ".webm",
                        ".opus",
                        ".mp4",
                        ".aac",
                        ".ogg",
                    )
                )
            ]

            if not media_files:
                raise FileNotFoundError(
                    "yt-dlp completed, but no audio file was found."
                )

            print(f"Audio downloaded using {client_name} client.")

            return media_files[0]
        except Exception as error:
            last_error = error

            logger.debug("Audio download attempt failed: %s", error)

    raise RuntimeError(
        "Failed to download YouTube audio. "
        "Make sure yt-dlp and FFmpeg are installed "
        "and that the video is publicly accessible.\n"
        "If YouTube blocks the request, export a cookies.txt file "
        "(Netscape format) from your browser and place it in the "
        "project folder.\n"
        f"Details: {last_error}"
    ) from last_error


def transcribe_audio(
    audio_path: str,
    language: str | None = None,
) -> dict:
    model = get_whisper_model()

    print("\nTranscribing audio with Whisper...")

    try:
        segments, info = model.transcribe(
            audio_path,
            language=language,
            vad_filter=True,
            beam_size=5,
        )

        entries = []

        for segment in segments:
            text = segment.text.strip()

            if not text:
                continue

            entries.append(
                {
                    "text": text,
                    "start": float(segment.start),
                    "duration": float(segment.end - segment.start),
                }
            )

        text = " ".join(entry["text"] for entry in entries)

        if not text.strip():
            raise RuntimeError("Whisper returned an empty transcript.")

        detected_language = getattr(
            info,
            "language",
            None,
        )

        return {
            "text": text.strip(),
            "entries": entries,
            "language": detected_language,
        }
    except Exception as error:
        raise RuntimeError(f"Whisper transcription failed: {error}") from error


def transcribe_youtube_audio(
    url: str,
    language: str | None = None,
) -> dict:
    temp_dir = tempfile.mkdtemp(prefix="notesmaker_")

    audio_path = None

    try:
        audio_path = download_audio(
            url=url,
            output_dir=temp_dir,
        )

        whisper_language = None if language == "en" else language

        result = transcribe_audio(
            audio_path=audio_path,
            language=whisper_language,
        )

        return result
    finally:
        try:
            for filename in os.listdir(temp_dir):
                filepath = os.path.join(
                    temp_dir,
                    filename,
                )

                if os.path.isfile(filepath):
                    os.remove(filepath)

            os.rmdir(temp_dir)
        except Exception as cleanup_error:
            logger.debug("Temporary file cleanup failed: %s", cleanup_error)
