from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from src.utils.config.config import YoutubeConfig
from src.utils.config.container import DependencyContainer
from src.utils.validation.languages import SupportedLanguages
from src.utils.io.video import extract_video_id


@dataclass
class TranscriptFetcher:
    video_id: str
    youtube_url: str
    youtube_language: SupportedLanguages

    def __init__(self, youtube_config: YoutubeConfig, dependencies: DependencyContainer):
        self.youtube_language = youtube_config.language
        self.youtube_url = youtube_config.url
        self.dependencies = dependencies
        self.youtube_video_id = extract_video_id(self.youtube_url)
        self.youtube_transcript_api = YouTubeTranscriptApi()
        self.youtube_transcriber = youtube_config.transcriber

    def fetch_transcript_text_from_youtube_api(self) -> str:
        print("Trying to fetch transcript from YouTube API...")
        transcript = self.youtube_transcript_api.fetch(
            self.youtube_video_id,
            languages=[self.youtube_language.language_code]
        )

        return "\n".join(
            snippet.text.replace("\n", " ").strip()
            for snippet in transcript
        )

    def fetch_transcript_text_from_audio(self) -> str:
        print("Falling back to audio transcription...")
        return self.youtube_transcriber.transcribe()

    def fetch_transcript(self) -> tuple[str, str]:
        try:
            script = self.fetch_transcript_text_from_youtube_api()
        except Exception:
            script = self.fetch_transcript_text_from_audio()

        return script, self.youtube_video_id
