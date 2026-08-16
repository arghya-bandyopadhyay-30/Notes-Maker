from faster_whisper.transcribe import Segment


def process_segment(segment: Segment) -> str:
    text = segment.text.strip()

    print(
        f"[{segment.start:.2f}s -> {segment.end:.2f}s] "
        f"{text}"
    )

    return text
