def format_time(seconds: float) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{int(hours)}h {int(minutes)}m {seconds:.3f}s"
