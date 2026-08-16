from utils.app_config_service import AppConfigService
from utils.dependency_container import DependencyContainer
from utils.file_system import FileSystem
from utils.video_id import extract_video_id
from utils.supported_languages import SupportedLanguage
from youtube_transcript.transcript_fetcher import TranscriptFetcher

CONFIG_PATH = "config.yaml"


def run(
    transcript_fetcher: TranscriptFetcher,
    youtube_language: SupportedLanguage,
    transcript_model: str,
    validator_model: str
):
    script = transcript_fetcher.fetch_transcript_text_from_audio()
    print("Script: ", script)

    translate = validate = not (youtube_language == SupportedLanguage.ENGLISH)
    print("Do we need to translate? ", translate)
    print("Do we need to validate? ", validate)


def main():
    dependencies = DependencyContainer(
        file_system=FileSystem(),
    )

    if not dependencies.file_system.path_exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}")
        return

    config = AppConfigService(
        dependencies=dependencies,
        config_path=CONFIG_PATH,
    ).get_config()

    transcript_fetcher = TranscriptFetcher(
        youtube_url=config.youtube.url,
        youtube_language=config.youtube.language
    )

    run(
        transcript_fetcher=transcript_fetcher,
        youtube_language=config.youtube.language,
        transcript_model=config.models.transcript,
        validator_model=config.models.validator
    )

    dependencies.file_system.make_dirs(config.output_directory)


if __name__ == "__main__":
    main()
