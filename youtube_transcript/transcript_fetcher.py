from dataclasses import dataclass

from utils.supported_languages import SupportedLanguage
from utils.video_id import extract_video_id


@dataclass
class TranscriptFetcher:
    video_id: str
    youtube_url: str
    youtube_language: SupportedLanguage

    def __init__(self, youtube_url: str, youtube_language: SupportedLanguage):
        self.youtube_language = youtube_language
        self.youtube_url = youtube_url
        self.video_id = extract_video_id(youtube_url)

