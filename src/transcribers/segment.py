from faster_whisper.transcribe import Segment

from src.utils.formatting.strings import SEGMENT_PRINT_FORMAT


def process_segment(segment: Segment) -> str:
    text = segment.text.strip()

    print(SEGMENT_PRINT_FORMAT.format(segment.start, segment.end, text))

    return text
