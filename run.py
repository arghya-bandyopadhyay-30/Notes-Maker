from pipeline_statistics.timing_tracker import timing_tracker
from processors.translator import Translator
from processors.validator import Validator
from prompt_factory.prompt_factory import PromptFactory
from utils.app_config_service import AppConfigService
from utils.dependency_container import DependencyContainer
from youtube_transcript.transcript_fetcher import TranscriptFetcher

CONFIG_PATH = "config.yaml"


def run(
    transcript_fetcher: TranscriptFetcher,
    translator: Translator,
    validator: Validator
) -> tuple[str, str]:
    try:
        original_script, video_id = (
            transcript_fetcher.fetch_transcript_text_from_youtube_api()
        )
    except Exception:
        original_script, video_id = (
            transcript_fetcher.fetch_transcript_text_from_audio()
        )

    print("Original Script:\n", original_script)

    translated_script = translator.translate(original_script=original_script)
    print("Translated Script:\n", translated_script)

    validation_score = validator.validate(original_script=original_script, translated_script=translated_script)

    return original_script, video_id


def main():
    dependencies = DependencyContainer()

    if not dependencies.file_system.path_exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}")
        return

    config = AppConfigService(
        dependencies=dependencies,
        config_path=CONFIG_PATH,
    ).get_config()

    file_system = dependencies.file_system
    file_system.make_dirs(config.output_directory)

    transcript_fetcher = TranscriptFetcher(
        youtube_config=config.youtube,
        dependencies=dependencies
    )

    prompt_factory = PromptFactory(
        file_system=dependencies.file_system
    )

    translator = Translator(
        youtube_language=config.youtube.language,
        llm=config.llm,
        prompt_factory=prompt_factory
    )

    validator = Validator(
        youtube_language=config.youtube.language,
        llm=config.llm,
        prompt_factory=prompt_factory
    )

    script, video_id = run(
        transcript_fetcher=transcript_fetcher,
        translator=translator,
        validator=validator
    )

    file_system.write_file(f"{config.output_directory}/{video_id}.txt", script)
    file_system.write_yaml(f"{config.output_directory}/pipeline_statistics.yaml", timing_tracker.to_dict())


if __name__ == "__main__":
    main()
