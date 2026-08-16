from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from transcribers.get_transcriber import get_transcriber
from utils.dependency_container import DependencyContainer
from utils.supported_languages import SupportedLanguage
from utils.video_id import extract_video_id


@dataclass
class TranscriptFetcher:
    video_id: str
    youtube_url: str
    youtube_language: str

    def __init__(self, youtube_url: str, youtube_language: SupportedLanguage, dependencies: DependencyContainer):
        self.youtube_language = youtube_language.value
        self.youtube_url = youtube_url
        self.dependencies = dependencies
        self.youtube_video_id = extract_video_id(youtube_url)
        self.youtube_transcript_api = YouTubeTranscriptApi()
        self.youtube_transcriber = get_transcriber(
            language=self.youtube_language,
            url=self.youtube_url,
            environment_system=self.dependencies.environment_system
        )

    def fetch_transcript_text_from_youtube_api(self) -> str:
        transcript = self.youtube_transcript_api.fetch(
            self.youtube_video_id,
            languages=[self.youtube_language]
        )

        return "\n".join(
            snippet.text.replace("\n", " ").strip()
            for snippet in transcript
        )

    def fetch_transcript_text_from_audio(self) -> str:
        return self.youtube_transcriber.transcribe()
