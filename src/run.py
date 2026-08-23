import asyncio

from src.pipeline.statistics.execution import execution_time
from src.pipeline.statistics.tracker import timing_tracker
from src.processors.processor import Processor
from src.utils.config.config_service import AppConfigService
from src.utils.config.container import DependencyContainer
from src.youtube.transcript import TranscriptFetcher

CONFIG_PATH = "config.yaml"

@execution_time
async def run(
    transcript_fetcher: TranscriptFetcher,
    processor: Processor
) -> tuple[str, str]:
    original_script, video_id = transcript_fetcher.fetch_transcript()
    final_script = await processor.process(original_script)
    return final_script.to_string(), video_id

@execution_time
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

    processor = Processor(
        youtube_language=app_config.youtube.language,
        llm=app_config.llm,
        prompt_factory=dependencies.prompt_factory
    )


    try:
        script, video_id = await run(
            transcript_fetcher=transcript_fetcher,
            processor=processor
        )
        file_system.write_file(f"{app_config.output_directory}/{video_id}.txt", script)
    finally:
        file_system.write_yaml(f"{app_config.output_directory}/pipeline_statistics.yaml", timing_tracker.to_dict())
        app_config.llm.provider.close()


if __name__ == "__main__":
    asyncio.run(main())
