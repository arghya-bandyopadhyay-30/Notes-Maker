import asyncio

from src.pipeline.statistics.tracker import timing_tracker
from src.processors.processor import Processor
from src.prompts.factory import PromptFactory
from src.utils.config.config_service import AppConfigService
from src.utils.config.container import DependencyContainer
from src.youtube.transcript import TranscriptFetcher

CONFIG_PATH = "config.yaml"


async def run(
    transcript_fetcher: TranscriptFetcher,
    processor: Processor
) -> tuple[str, str]:
    original_script, video_id = transcript_fetcher.fetch_transcript()
    translated_script, validation_score = await processor.process(original_script)
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

    processor = Processor(
        youtube_language=app_config.youtube.language,
        llm=app_config.llm,
        prompt_factory=prompt_factory
    )

    script, video_id = await run(
        transcript_fetcher=transcript_fetcher,
        processor=processor
    )

    file_system.write_file(f"{app_config.output_directory}/{video_id}.txt", script)
    file_system.write_yaml(f"{app_config.output_directory}/pipeline_statistics.yaml", timing_tracker.to_dict())

    app_config.llm.provider.close()


if __name__ == "__main__":
    asyncio.run(main())
