import yt_dlp

YOUTUBE_URL = "https://www.youtube.com/watch?v=q9jixKv4h2I"

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": f"audio_directory/%(id)s.%(ext)s",
    "js_runtimes": {"node": {"path": "C:/Program Files/node.exe"}},
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
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(
        YOUTUBE_URL,
        download=True,
    )

video_id = info["id"]

import whisper


AUDIO_PATH = f"audio_directory/{video_id}.wav"

print("Loading Whisper model...")

model = whisper.load_model("small")


print("Starting transcription...")

result = model.transcribe(
    AUDIO_PATH,
    language="en",
    task="transcribe",
    fp16=False,
)


print("\nTranscript:\n")

print(result["text"])