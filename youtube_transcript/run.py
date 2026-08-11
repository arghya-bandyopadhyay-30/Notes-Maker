import os
import sys

from youtube_transcript import (
    SUPPORTED_LANGUAGES,
    extract_video_id,
    fetch_transcript,
)


def save_transcript_to_file(
    transcript: str,
    video_id: str,
    language: str,
    output_dir: str = "output",
) -> str:
    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    filename = f"{video_id}_{language}_transcript.txt"

    filepath = os.path.join(
        output_dir,
        filename,
    )

    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(transcript)

    return filepath


def select_language() -> str:
    print("\nAvailable languages:")

    for code, name in SUPPORTED_LANGUAGES.items():
        print(f"  {code}: {name}")

    while True:
        choice = input("\nSelect language (en/hi/bn) [default: en]: ").strip().lower()

        if not choice:
            return "en"

        if choice in SUPPORTED_LANGUAGES:
            return choice

        print(f"Invalid choice. Select from: {list(SUPPORTED_LANGUAGES.keys())}")


def run(
    url: str,
    language: str = "en",
    translate: bool = True,
    validate: bool = True,
    output_dir: str = "output",
):
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL or video ID.")

    print(f"\nVideo ID: {video_id}")
    print(f"\nRequested language: {SUPPORTED_LANGUAGES.get(language, language)}")

    if translate and language != "en":
        print("Translation to English: ENABLED")
        print("Translation validation: " + ("ENABLED" if validate else "DISABLED"))
    else:
        print("Translation: DISABLED")

    print("\nStarting transcript pipeline...")

    result = fetch_transcript(
        url=url,
        language=language,
        translate=translate,
        validate=validate,
    )

    transcript = result["transcript"]
    original_transcript = result.get("original_transcript")
    translated_transcript = result.get("translated_transcript")
    score = result.get("validation_score")
    reason = result.get("validation_reason")
    passed = result.get("passed_validation")
    used_original = result.get("used_original", False)
    source = result.get("source", "unknown")

    filepath = save_transcript_to_file(
        transcript=transcript,
        video_id=video_id,
        language=language,
        output_dir=output_dir,
    )

    print(f"\nTranscript saved to:")
    print(f"  {os.path.abspath(filepath)}")
    print(f"\nTranscript source: {source}")

    if score is not None:
        print(f"\nValidation Score: {score}/100")
        print("Validation: " + ("PASSED" if passed else "FAILED"))
        print(f"Reason: {reason}")

    print("\n" + "=" * 60)
    print("TRANSCRIPT PREVIEW")
    print("=" * 60)

    if used_original:
        print(f"\nOriginal {SUPPORTED_LANGUAGES[language]} transcript:\n")
        print(original_transcript[:1500])

        if translated_transcript:
            print("\n" + "-" * 60)
            print("REJECTED ENGLISH TRANSLATION")
            print("-" * 60)
            print(translated_transcript[:1000])
    else:
        preview = transcript[:1500]

        if len(transcript) > 1500:
            preview += "..."

        print(preview)

    print("\n" + "=" * 60)

    return result


def interactive_mode():
    print("\n" + "=" * 60)
    print("NOTES MAKER")
    print("YouTube Transcript Fetcher")
    print("=" * 60)

    url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("Error: URL cannot be empty.")
        return

    video_id = extract_video_id(url)

    if not video_id:
        print("Error: Invalid YouTube URL.")
        return

    print(f"\nVideo ID: {video_id}")

    language = select_language()

    translate = True
    validate = True

    if language != "en":
        translate_choice = (
            input("\nTranslate to English? (y/n) [default: y]: ").strip().lower()
        )
        translate = translate_choice != "n"

        if translate:
            validate_choice = (
                input("Validate translation quality? (y/n) [default: y]: ")
                .strip()
                .lower()
            )
            validate = validate_choice != "n"

    try:
        run(
            url=url,
            language=language,
            translate=translate,
            validate=validate,
        )
    except Exception as error:
        print("\nERROR")
        print("-" * 60)
        print(str(error))


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            url = sys.argv[1]
            language = "en"

            if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
                language = sys.argv[2].strip().lower()

            translate = "--no-translate" not in sys.argv
            validate = "--no-validate" not in sys.argv

            run(
                url=url,
                language=language,
                translate=translate,
                validate=validate,
            )
        else:
            interactive_mode()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as error:
        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)
        print(str(error))
        sys.exit(1)
