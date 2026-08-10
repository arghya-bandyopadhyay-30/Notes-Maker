import os
import sys
from youtube_transcript import (
    fetch_transcript,
    extract_video_id,
    list_available_transcripts,
    SUPPORTED_LANGUAGES,
)


def save_transcript_to_file(transcript: str, video_id: str, language: str, output_dir: str = "output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{video_id}_{language}_transcript.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(transcript)
    
    return filepath


def select_language() -> str:
    print("\nAvailable languages:")
    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"  {code}: {name}")
    
    while True:
        choice = input("Select language (en/hi/bn) [default: en]: ").strip().lower()
        if not choice:
            return "en"
        if choice in SUPPORTED_LANGUAGES:
            return choice
        print(f"Invalid choice. Please select from: {list(SUPPORTED_LANGUAGES.keys())}")


def run(url: str, language: str = "en", translate: bool = True, validate: bool = True, output_dir: str = "output"):
    """
    Main function to fetch transcript from a YouTube URL.
    Can be called programmatically or from CLI.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID")
    
    print(f"\nVideo ID: {video_id}")
    
    # Show available transcripts
    try:
        available = list_available_transcripts(url)
        print("\nAvailable transcripts:")
        for t in available:
            gen = " (auto-generated)" if t["is_generated"] else ""
            trans = " (translatable)" if t["is_translatable"] else ""
            print(f"  {t['language_code']}: {t['language']}{gen}{trans}")
    except ValueError as e:
        print(f"Could not list transcripts: {e}")
    
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}. Supported: {list(SUPPORTED_LANGUAGES.keys())}")
    
    print(f"\nFetching transcript in {SUPPORTED_LANGUAGES[language]}...")
    if translate and language != "en":
        print("Translation to English enabled (using Ollama)...")
        if validate:
            print("Translation validation enabled (requires Ollama)...")
    
    result = fetch_transcript(url, language=language, translate=translate, validate=validate)
    
    transcript = result["transcript"]
    original_transcript = result.get("original_transcript")
    translated_transcript = result.get("translated_transcript")
    score = result.get("validation_score")
    reason = result.get("validation_reason")
    passed = result.get("passed_validation")
    used_original = result.get("used_original", False)
    
    filepath = save_transcript_to_file(transcript, video_id, language, output_dir)
    print(f"\nTranscript saved to: {filepath}")
    
    if score is not None:
        print(f"Validation Score: {score}/100")
        print(f"Validation: {'PASSED' if passed else 'FAILED'}")
        print(f"Reason: {reason}")
    
    if used_original:
        print(f"\n--- Original {SUPPORTED_LANGUAGES[language]} Transcript ---")
        print(original_transcript)
        if translated_transcript:
            print(f"\n--- Rejected English Translation (Score: {score}/100) ---")
            preview = translated_transcript[:500] + "..." if len(translated_transcript) > 500 else translated_transcript
            print(preview)
    else:
        preview = transcript[:500] + "..." if len(transcript) > 500 else transcript
        print(f"\nPreview:\n{preview}")
    
    return result


def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "="*50)
    print("NOTES MAKER - YouTube Transcript Fetcher")
    print("="*50)
    
    url = input("Enter YouTube URL: ").strip()
    if not url:
        print("Error: URL cannot be empty")
        return
    
    video_id = extract_video_id(url)
    if not video_id:
        print("Error: Invalid YouTube URL")
        return
    
    print(f"\nVideo ID: {video_id}")
    
    # Show available transcripts
    try:
        available = list_available_transcripts(url)
        print("\nAvailable transcripts:")
        for t in available:
            gen = " (auto-generated)" if t["is_generated"] else ""
            trans = " (translatable)" if t["is_translatable"] else ""
            print(f"  {t['language_code']}: {t['language']}{gen}{trans}")
    except ValueError as e:
        print(f"Could not list transcripts: {e}")
    
    language = select_language()
    
    translate = True
    validate = True
    if language != "en":
        translate_choice = input("Translate to English? (y/n) [default: y]: ").strip().lower()
        translate = translate_choice != "n"
        
        if translate:
            validate_choice = input("Validate translation quality? (y/n) [default: y]: ").strip().lower()
            validate = validate_choice != "n"
    
    run(url, language=language, translate=translate, validate=validate)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode: python -m youtube_transcript.run <url> [language] [--no-translate] [--no-validate]
        url = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "en"
        translate = "--no-translate" not in sys.argv
        validate = "--no-validate" not in sys.argv
        run(url, language=language, translate=translate, validate=validate)
    else:
        interactive_mode()