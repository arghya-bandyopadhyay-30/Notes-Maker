from dataclasses import dataclass

from youtube_transcript_api import YouTubeTranscriptApi

from src.pipeline.statistics.execution import execution_time
from src.utils.config.youtube_config import YoutubeConfig
from src.utils.config.dependency_container import DependencyContainer
from src.utils.formatting.strings import (
    TRYING_FETCH_TRANSCRIPT_API,
    FALLING_BACK_AUDIO_TRANSCRIPTION,
    TRANSCRIPT_JOIN_SEPARATOR,
)
from src.utils.validation.supported_languages import SupportedLanguages
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
        print(TRYING_FETCH_TRANSCRIPT_API)
        transcript = self.youtube_transcript_api.fetch(
            self.youtube_video_id,
            languages=[self.youtube_language.language_code]
        )

        return TRANSCRIPT_JOIN_SEPARATOR.join(
            snippet.text.replace(TRANSCRIPT_JOIN_SEPARATOR, " ").strip()
            for snippet in transcript
        )

    def fetch_transcript_text_from_audio(self) -> str:
        print(FALLING_BACK_AUDIO_TRANSCRIPTION)
        return self.youtube_transcriber.transcribe()

    @execution_time
    def fetch_transcript(self) -> tuple[str, str]:
        try:
            script = self.fetch_transcript_text_from_youtube_api()
        except Exception:
            script = self.fetch_transcript_text_from_audio()

        return script, self.youtube_video_id
