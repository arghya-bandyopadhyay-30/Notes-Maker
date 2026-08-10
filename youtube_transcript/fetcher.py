import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

from .translator import (
    translate_to_english, 
    translate_transcript_entries, 
    validate_translation
)


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
}

# YouTube transcript formatting markers to remove
FORMATTING_PATTERN = re.compile(r'[\u0000-\u001f\u007f-\u009f]')  # Control characters
MUSIC_NOTE_PATTERN = re.compile(r'\u266a')  # ♫ musical note used as formatting marker
BRACKET_PATTERN = re.compile(r'[\[\]()]')  # Brackets


def clean_transcript_text(text: str) -> str:
    text = FORMATTING_PATTERN.sub('', text)
    text = MUSIC_NOTE_PATTERN.sub('', text)
    text = BRACKET_PATTERN.sub('', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_video_id(url: str) -> Optional[str]:
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(url: str, language: str = "en", translate: bool = True, validate: bool = True) -> dict:
    """
    Fetch transcript with optional translation and validation.
    Returns dict with: transcript, original_transcript, validation_score, validation_reason, passed_validation, used_original
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID")

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=[language])
        original_transcript = " ".join([clean_transcript_text(snippet.text) for snippet in transcript])

        if translate and language != "en":
            translated_transcript = translate_to_english(original_transcript, language)
            
            if validate:
                validation = validate_translation(original_transcript, translated_transcript, language)
                score = validation["score"]
                reason = validation["reason"]
                passed = score >= 90
                
                print(f"\nValidation Score: {score}/100")
                print(f"Validation Result: {'PASSED' if passed else 'FAILED'}")
                print(f"Reason: {reason}")
                
                if not passed:
                    print(f"\nValidation failed. Using original {SUPPORTED_LANGUAGES[language]} transcript.")
                    return {
                        "transcript": original_transcript,
                        "original_transcript": original_transcript,
                        "translated_transcript": translated_transcript,
                        "validation_score": score,
                        "validation_reason": reason,
                        "passed_validation": False,
                        "used_original": True
                    }
                
                return {
                    "transcript": translated_transcript,
                    "original_transcript": original_transcript,
                    "translated_transcript": translated_transcript,
                    "validation_score": score,
                    "validation_reason": reason,
                    "passed_validation": True,
                    "used_original": False
                }
            else:
                return {
                    "transcript": translated_transcript,
                    "original_transcript": original_transcript,
                    "translated_transcript": translated_transcript,
                    "validation_score": None,
                    "validation_reason": "Validation skipped",
                    "passed_validation": True,
                    "used_original": False
                }
        else:
            return {
                "transcript": original_transcript,
                "original_transcript": original_transcript,
                "translated_transcript": None,
                "validation_score": 100,
                "validation_reason": "No translation needed (English)",
                "passed_validation": True,
                "used_original": False
            }
    except TranscriptsDisabled:
        raise ValueError(f"Transcripts are disabled for video: {video_id}")
    except NoTranscriptFound:
        available = list_available_transcripts(url)
        available_langs = [t["language_code"] for t in available]
        raise ValueError(f"No transcript found for video: {video_id} in language: {language}. Available: {available_langs}")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")


def fetch_transcript_with_timestamps(url: str, language: str = "en", translate: bool = True, validate: bool = True) -> dict:
    """
    Fetch transcript with timestamps, optional translation and validation.
    Returns dict with: entries, validation_score, validation_reason, passed_validation
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID")

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=[language])
        original_entries = [
            {
                "text": clean_transcript_text(snippet.text),
                "start": snippet.start,
                "duration": snippet.duration,
            }
            for snippet in transcript
        ]
        original_text = " ".join([e["text"] for e in original_entries])

        if translate and language != "en":
            translated_entries = translate_transcript_entries(original_entries, language)
            translated_text = " ".join([e["text"] for e in translated_entries])
            
            if validate:
                validation = validate_translation(original_text, translated_text, language)
                score = validation["score"]
                reason = validation["reason"]
                passed = score >= 90
                
                print(f"\nValidation Score: {score}/100")
                print(f"Validation Result: {'PASSED' if passed else 'FAILED'}")
                print(f"Reason: {reason}")
                
                if not passed:
                    raise ValueError(f"Translation validation failed (score: {score}/100). Reason: {reason}")
                
                return {
                    "entries": translated_entries,
                    "original_entries": original_entries,
                    "validation_score": score,
                    "validation_reason": reason,
                    "passed_validation": True
                }
            else:
                return {
                    "entries": translated_entries,
                    "original_entries": original_entries,
                    "validation_score": None,
                    "validation_reason": "Validation skipped",
                    "passed_validation": True
                }
        else:
            return {
                "entries": original_entries,
                "original_entries": original_entries,
                "validation_score": 100,
                "validation_reason": "No translation needed (English)",
                "passed_validation": True
            }
    except TranscriptsDisabled:
        raise ValueError(f"Transcripts are disabled for video: {video_id}")
    except NoTranscriptFound:
        available = list_available_transcripts(url)
        available_langs = [t["language_code"] for t in available]
        raise ValueError(f"No transcript found for video: {video_id} in language: {language}. Available: {available_langs}")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")


def list_available_transcripts(url: str) -> list:
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID")

    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        return [
            {
                "language": t.language,
                "language_code": t.language_code,
                "is_generated": t.is_generated,
                "is_translatable": len(t.translation_languages) > 0,
            }
            for t in transcript_list
        ]
    except Exception as e:
        raise ValueError(f"Error listing transcripts: {str(e)}")