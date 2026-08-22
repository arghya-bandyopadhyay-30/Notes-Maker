import sys
import asyncio

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from src.pipeline.statistics.tracker import timing_tracker
from src.processors.translator import Translator
from src.processors.validator import Validator
from src.prompts.factory import PromptFactory
from src.utils.config_service import AppConfigService
from src.utils.container import DependencyContainer
from src.youtube.transcript import TranscriptFetcher

CONFIG_PATH = "config.yaml"


async def run(
    transcript_fetcher: TranscriptFetcher,
    translator: Translator,
    validator: Validator
) -> tuple[str, str]:
    original_script, video_id = transcript_fetcher.fetch_transcript()
    print("Original Script:\n", original_script)

    translated_script = await translator.translate(original_script=original_script)
    print("Translated Script:\n", translated_script)

    validation_score = validator.validate(original_script=original_script, translated_script=translated_script)
    print("Validation Script:\n", validation_score)

    return translated_script, video_id


async def main():
    dependencies = DependencyContainer()

    if not dependencies.file_system.path_exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}")
        return

    app_config = AppConfigService(
        dependencies=dependencies,
        config_path=CONFIG_PATH,
    ).get_config()

    file_system = dependencies.file_system
    file_system.make_dirs(app_config.output_directory)

    transcript_fetcher = TranscriptFetcher(
        youtube_config=app_config.youtube,
        dependencies=dependencies
    )

    prompt_factory = PromptFactory(
        file_system=dependencies.file_system
    )

    translator = Translator(
        youtube_language=app_config.youtube.language,
        llm=app_config.llm,
        prompt_factory=prompt_factory
    )

    validator = Validator(
        youtube_language=app_config.youtube.language,
        llm=app_config.llm,
        prompt_factory=prompt_factory
    )

    script, video_id = await run(
        transcript_fetcher=transcript_fetcher,
        translator=translator,
        validator=validator
    )

    file_system.write_file(f"{app_config.output_directory}/{video_id}.txt", script)
    file_system.write_yaml(f"{app_config.output_directory}/pipeline_statistics.yaml", timing_tracker.to_dict())

    app_config.llm.provider.close()


if __name__ == "__main__":
    asyncio.run(main())
