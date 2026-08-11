from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from utils.supported_languages import SupportedLanguage
from utils.video_id import extract_video_id


@dataclass
class TranscriptFetcher:
    video_id: str
    youtube_url: str
    youtube_language: str

    def __init__(self, youtube_url: str, youtube_language: SupportedLanguage):
        self.youtube_language = youtube_language.value
        self.youtube_url = youtube_url
        self.youtube_video_id = extract_video_id(youtube_url)
        self.youtube_transcript_api = YouTubeTranscriptApi()

    def fetch_transcript_text(self) -> str:
        transcript = self.youtube_transcript_api.fetch(
            self.youtube_video_id,
            languages=[self.youtube_language]
        )

        return "\n".join(
            snippet.text.replace("\n", " ").strip()
            for snippet in transcript
        )
