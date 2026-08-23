import asyncio

from src.bootstrap.container import DependencyContainer
from src.pipeline.execution import execution_time
from src.pipeline.timing_tracker import timing_tracker
from src.processors.processor import Processor
from src.utils.config.app_config_service import AppConfigService
from src.utils.formatting.strings import (
    CONFIG_FILE_NAME,
    CONFIG_FILE_NOT_FOUND,
    OUTPUT_SCRIPT_FILE_PATTERN,
    OUTPUT_STATISTICS_FILE_PATTERN,
)
from src.youtube.transcript_fetcher import TranscriptFetcher


@execution_time
async def run(
    transcript_fetcher: TranscriptFetcher, processor: Processor, validation_threshold: float
) -> tuple[str, str]:
    original_script, video_id = transcript_fetcher.fetch_transcript()
    final_script = await processor.process(original_script)
    return (final_script.to_string(validation_threshold=validation_threshold), video_id)


async def main():
    dependencies = DependencyContainer()

    if not dependencies.file_system.path_exists(CONFIG_FILE_NAME):
        print(CONFIG_FILE_NOT_FOUND.format(CONFIG_FILE_NAME))
        return

    app_config = AppConfigService(
        dependencies=dependencies,
        config_path=CONFIG_FILE_NAME,
    ).get_config()

    file_system = dependencies.file_system
    file_system.make_dirs(app_config.output_directory)

    transcript_fetcher = TranscriptFetcher(
        youtube_config=app_config.youtube, dependencies=dependencies
    )

    processor = Processor(
        youtube_language=app_config.youtube.language,
        llm=app_config.llm,
        prompt_factory=dependencies.prompt_factory,
    )

    try:
        script, video_id = await run(
            transcript_fetcher=transcript_fetcher,
            processor=processor,
            validation_threshold=app_config.llm.validation_threshold,
        )
        file_system.write_file(
            OUTPUT_SCRIPT_FILE_PATTERN.format(app_config.output_directory, video_id), script
        )
    finally:
        file_system.write_yaml(
            OUTPUT_STATISTICS_FILE_PATTERN.format(app_config.output_directory),
            timing_tracker.to_dict(),
        )
        app_config.llm.provider.close()
        app_config.youtube.transcriber.close()


if __name__ == "__main__":
    asyncio.run(main())
