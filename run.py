from utils.app_config_service import AppConfigService
from utils.file_system import FileSystem


def main():
    config = AppConfigService(
        file_system=FileSystem(),
        config_path="config.yaml",
    ).get_config()

    print(config)


if __name__ == "__main__":
    main()
