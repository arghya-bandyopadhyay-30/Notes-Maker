import yt_dlp

YOUTUBE_URL = "https://www.youtube.com/watch?v=4cm9PMNikXM"

# def download_audio_as_mp3(url: str, output_dir: str = "audio"):
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
#         "js_runtimes": {"node": {"path": "C:/Program Files/node.exe"}},
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "192",
#             }
#         ],
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# download_audio_as_mp3(YOUTUBE_URL)

# from banglaspeech2text import Speech2Text
#
#
# AUDIO_PATH = "audio/4cm9PMNikXM.mp3"
#
#
# print("Loading BanglaSpeech2Text model...")
#
# stt = Speech2Text("small")
#
# print("Model loaded.")
# print("Starting transcription...\n")
#
#
# segments = stt.recognize(
#     AUDIO_PATH,
#     return_segments=True
# )
#
#
# transcript = []
#
# for segment in segments:
#     text = segment.text.strip()
#
#     print(
#         f"[{segment.start:.2f}s -> {segment.end:.2f}s] "
#         f"{text}"
#     )
#
#     transcript.append(text)
#
#
# final_transcript = " ".join(transcript)
#
# print("\nFinal Transcript:\n")
# print(final_transcript)