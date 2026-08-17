from processors.translator import Translator
from processors.validator import Validator
from utils.app_config_service import AppConfigService
from utils.dependency_container import DependencyContainer
from utils.supported_languages import SupportedLanguage
from youtube_transcript.transcript_fetcher import TranscriptFetcher

CONFIG_PATH = "config.yaml"


def run(
    transcript_fetcher: TranscriptFetcher,
    translator: Translator,
    validator: Validator
) -> tuple[str, str]:
    try:
        print("Trying to fetch transcript from YouTube API...")
        script, video_id = (
            transcript_fetcher.fetch_transcript_text_from_youtube_api()
        )
    except Exception:
        print("Falling back to audio transcription...")
        script, video_id = (
            transcript_fetcher.fetch_transcript_text_from_audio()
        )

    return script, video_id


def main():
    dependencies = DependencyContainer()

    if not dependencies.file_system.path_exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}")
        return

    config = AppConfigService(
        dependencies=dependencies,
        config_path=CONFIG_PATH,
    ).get_config()

    transcript_fetcher = TranscriptFetcher(
        youtube_url=config.youtube.url,
        youtube_language=config.youtube.language,
        dependencies=dependencies
    )

    translator = Translator(
        youtube_language=config.youtube.language,
        model=config.models.translator,
        environment_system=dependencies.environment_system
    )

    validator = Validator(
        youtube_language=config.youtube.language,
        model=config.models.validator,
        environment_system=dependencies.environment_system
    )

    script, video_id = run(
        transcript_fetcher=transcript_fetcher,
        translator=translator,
        validator=validator
    )

    file_system = dependencies.file_system
    file_system.make_dirs(config.output_directory)
    file_system.write_file(f"{config.output_directory}/{video_id}.txt", script)


if __name__ == "__main__":
    main()
