from faster_whisper.transcribe import Segment


def process_segment(segment: Segment):
    text = segment.text.strip()

    print(
        f"[{segment.start:.2f}s -> "
        f"{segment.end:.2f}s] "
        f"{text}"
    )

    return text
