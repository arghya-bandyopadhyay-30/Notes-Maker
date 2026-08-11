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


def extract_video_id(url: str) -> Optional[str]:
    if not url:
        return None

    url = url.strip()

    if len(url) >= 2 and url[0] == url[-1] and url[0] in {'"', "'"}:
        url = url[1:-1].strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    host = parsed.netloc.lower()

    if host.startswith("www."):
        host = host[4:]

    if host.startswith("m."):
        host = host[2:]

    if host == "youtube.com" and parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [None])[0]

        if video_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            return video_id

    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]

        if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            return video_id

    match = re.search(r"/(?:shorts|embed|v)/([A-Za-z0-9_-]{11})", parsed.path)

    if match:
        return match.group(1)

    return None


def fetch_from_transcript_api(
    video_id: str,
    language: str,
) -> list:
    api = YouTubeTranscriptApi()

    transcript = api.fetch(video_id, languages=[language])

    entries = []

    for snippet in transcript:
        text = clean_transcript_text(snippet.text)

        if not text:
            continue

        entries.append(
            {
                "text": text,
                "start": float(snippet.start),
                "duration": float(snippet.duration),
            }
        )

    if not entries:
        raise ValueError("YouTube returned an empty transcript.")

    return entries


def fetch_entries_with_fallback(
    url: str,
    video_id: str,
    language: str,
) -> tuple[list, str]:
    print("\nTrying YouTube transcript API...")

    try:
        entries = fetch_from_transcript_api(video_id, language)
        print("YouTube transcript retrieved successfully.")
        return entries, "youtube_transcript_api"
    except (TranscriptsDisabled, NoTranscriptFound) as error:
        print(f"Transcript unavailable: {type(error).__name__}")
    except Exception as error:
        error_name = type(error).__name__
        print(f"Transcript API failed: {error_name}")

        if "IpBlocked" in error_name:
            print("YouTube appears to be blocking the transcript request.")
        else:
            print(f"Reason: {str(error)[:300]}")

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


def fetch_transcript_with_timestamps(
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

    original_text = " ".join(entry["text"] for entry in entries)

    if language == "en" or not translate:
        reason = (
            "No translation needed (English)"
            if language == "en"
            else "Translation disabled"
        )

        return {
            "entries": entries,
            "original_entries": entries,
            "validation_score": 100,
            "validation_reason": reason,
            "passed_validation": True,
            "source": source,
        }

    print(f"\nTranslating timestamped {SUPPORTED_LANGUAGES[language]} transcript...")

    translated_entries = translate_transcript_entries(
        entries,
        language,
    )

    translated_text = " ".join(entry["text"] for entry in translated_entries)

    if validate:
        validation = validate_translation(
            original_text=original_text,
            translated_text=translated_text,
            source_lang=language,
        )

        score = validation["score"]
        reason = validation["reason"]
        passed = score >= 90

        print(f"\nValidation Score: {score}/100")
        print("Validation Result: " + ("PASSED" if passed else "FAILED"))
        print(f"Reason: {reason}")

        if not passed:
            raise ValueError(
                f"Translation validation failed (score: {score}/100). "
                f"Reason: {reason}"
            )

        return {
            "entries": translated_entries,
            "original_entries": entries,
            "validation_score": score,
            "validation_reason": reason,
            "passed_validation": True,
            "source": source,
        }

    return {
        "entries": translated_entries,
        "original_entries": entries,
        "validation_score": None,
        "validation_reason": "Validation skipped",
        "passed_validation": True,
        "source": source,
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
