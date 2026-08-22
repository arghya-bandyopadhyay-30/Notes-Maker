from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from utils.config import YoutubeConfig
from utils.dependency_container import DependencyContainer
from utils.supported_languages import SupportedLanguages
from utils.video_id import extract_video_id


@dataclass
class TranscriptFetcher:
    video_id: str
    youtube_url: str
    youtube_language: str

    def __init__(self, youtube_config: YoutubeConfig, dependencies: DependencyContainer):
        self.youtube_language = youtube_config.language.value
        self.youtube_url = youtube_config.url
        self.dependencies = dependencies
        self.youtube_video_id = extract_video_id(self.youtube_url)
        self.youtube_transcript_api = YouTubeTranscriptApi()
        self.youtube_transcriber = youtube_config.transcriber

    def fetch_transcript_text_from_youtube_api(self) -> tuple[str, str]:
        print("Trying to fetch transcript from YouTube API...")
        transcript = self.youtube_transcript_api.fetch(
            self.youtube_video_id,
            languages=[self.youtube_language]
        )

        script = "\n".join(
            snippet.text.replace("\n", " ").strip()
            for snippet in transcript
        )

        return script, self.youtube_video_id

    def fetch_transcript_text_from_audio(self) -> tuple[str, str]:
        print("Falling back to audio transcription...")
        script =  self.youtube_transcriber.transcribe()

        return script, self.youtube_video_id
