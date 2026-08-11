import re
from typing import Optional
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from .audio_fallback import transcribe_youtube_audio
from .translator import (
    translate_to_english,
    translate_transcript_entries,
    validate_translation,
)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
}

FORMATTING_PATTERN = re.compile(r"[\u0000-\u001f\u007f-\u009f]")

MUSIC_NOTE_PATTERN = re.compile(r"\u266a")

BRACKET_PATTERN = re.compile(r"[\[\]\(\)]")


def clean_transcript_text(text: str) -> str:
    if not text:
        return ""

    text = FORMATTING_PATTERN.sub("", text)
    text = MUSIC_NOTE_PATTERN.sub("", text)
    text = BRACKET_PATTERN.sub("", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def fetch_entries_with_fallback(
    url: str,
    video_id: str,
    language: str,
) -> tuple[list, str]:
    print("\nTrying YouTube transcript API...")
    print("\nFalling back to audio transcription...")

    try:
        result = transcribe_youtube_audio(
            url=url,
            language=language,
        )

        entries = result["entries"]

        if not entries:
            raise ValueError("Whisper produced an empty transcript.")

        print("Audio transcription completed.")

        return entries, "whisper"
    except Exception as error:
        raise ValueError(
            "All transcript providers failed.\n" f"Audio transcription error: {error}"
        ) from error


def fetch_transcript(
    url: str,
    language: str = "en",
    translate: bool = True,
    validate: bool = True,
) -> dict:
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID.")

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: {language}. "
            f"Supported: {list(SUPPORTED_LANGUAGES.keys())}"
        )

    entries, source = fetch_entries_with_fallback(
        url=url,
        video_id=video_id,
        language=language,
    )

    original_transcript = " ".join(entry["text"] for entry in entries)

    original_transcript = clean_transcript_text(original_transcript)

    if not original_transcript:
        raise ValueError("Transcript is empty.")

    print(f"\nTranscript source: {source}")
    print(f"Transcript length: {len(original_transcript):,} characters")

    if language == "en" or not translate:
        reason = (
            "No translation needed (English)"
            if language == "en"
            else "Translation disabled"
        )

        return {
            "transcript": original_transcript,
            "original_transcript": original_transcript,
            "translated_transcript": None,
            "validation_score": 100,
            "validation_reason": reason,
            "passed_validation": True,
            "used_original": False,
            "source": source,
            "entries": entries,
        }

    print(f"\nTranslating {SUPPORTED_LANGUAGES[language]} → English...")

    translated_transcript = translate_to_english(
        original_transcript,
        language,
    )

    if validate:
        print("\nValidating translation...")

        validation = validate_translation(
            original_text=original_transcript,
            translated_text=translated_transcript,
            source_lang=language,
        )

        score = validation["score"]
        reason = validation["reason"]
        passed = score >= 90

        print(f"Validation Score: {score}/100")
        print("Validation Result: " + ("PASSED" if passed else "FAILED"))
        print(f"Reason: {reason}")

        if not passed:
            print("\nTranslation validation failed.")
            print(f"Using original {SUPPORTED_LANGUAGES[language]} transcript.")

            return {
                "transcript": original_transcript,
                "original_transcript": original_transcript,
                "translated_transcript": translated_transcript,
                "validation_score": score,
                "validation_reason": reason,
                "passed_validation": False,
                "used_original": True,
                "source": source,
                "entries": entries,
            }

        return {
            "transcript": translated_transcript,
            "original_transcript": original_transcript,
            "translated_transcript": translated_transcript,
            "validation_score": score,
            "validation_reason": reason,
            "passed_validation": True,
            "used_original": False,
            "source": source,
            "entries": entries,
        }

    return {
        "transcript": translated_transcript,
        "original_transcript": original_transcript,
        "translated_transcript": translated_transcript,
        "validation_score": None,
        "validation_reason": "Validation skipped",
        "passed_validation": True,
        "used_original": False,
        "source": source,
        "entries": entries,
    }


def list_available_transcripts(url: str) -> list:
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID.")

    try:
        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)

        results = []

        for transcript in transcript_list:
            results.append(
                {
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": bool(transcript.translation_languages),
                }
            )

        return results
    except Exception as error:
        raise ValueError(f"Error listing transcripts: {error}") from error
