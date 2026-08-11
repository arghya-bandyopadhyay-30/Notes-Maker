from utils.app_config_service import AppConfigService
from utils.dependency_container import DependencyContainer
from utils.file_system import FileSystem
from utils.video_id import extract_video_id

CONFIG_PATH = "config.yaml"


def run(
    youtube_url: str,
    youtube_language: str
):
    video_id = extract_video_id(youtube_url)



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

    dependencies.file_system.make_dirs(config.output_directory)

    output_dir_path = config.output_directory
    youtube_url = config.youtube.url
    youtube_language = config.youtube.language
    transcript_model = config.models.transcript
    validator_model = config.models.validator

    run(
        youtube_url=youtube_url,
        youtube_language=youtube_language
    )


if __name__ == "__main__":
    main()
