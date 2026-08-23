from src.utils.formatting.strings import TIME_FORMAT


def format_time(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return TIME_FORMAT.format(int(hours), int(minutes), seconds)
