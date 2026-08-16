from banglaspeech2text import Speech2Text

from transcribers.transcriber import Transcriber
from utils.environment_system import EnvironmentSystem
from utils.process_segment import process_segment


class BnTranscriber(Transcriber):
    def __init__(self, url: str, environment_system: EnvironmentSystem):
        super().__init__(url=url, environment_system=environment_system)
        speech_to_text_model = Speech2Text("small")
        self.segments = speech_to_text_model.recognize(
            self.audio_path,
            return_segments=True
        )

    def transcribe(self) -> str:
        transcript = [
            process_segment(segment)
            for segment in self.segments
        ]

        return "\n".join(transcript)
