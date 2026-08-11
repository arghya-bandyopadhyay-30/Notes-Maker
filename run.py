from utils.app_config_service import AppConfigService
from utils.file_system import FileSystem

CONFIG_PATH = "config.yaml"


def main():
    file_system = FileSystem()

    if not file_system.path_exists(CONFIG_PATH):
        print(f"Config file not found: {CONFIG_PATH}")
        return

    config = AppConfigService(
        file_system=file_system,
        config_path=CONFIG_PATH,
    ).get_config()

    file_system.make_dir(config.output_directory)

    print(config)
    print(f"Output directory: {config.output_directory}")


if __name__ == "__main__":
    main()
