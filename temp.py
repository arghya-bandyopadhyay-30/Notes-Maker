from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()

transcript = api.fetch("oBfDbucxPU4", languages=["es"])
script = "\n\n".join(
    snippet.text.replace("\n", " ").strip()
    for snippet in transcript
)

print(script)