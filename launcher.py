import argparse
import os
import subprocess
import sys
import time

from start import (
    check_model_pulled,
    check_ollama_running,
    pull_model,
    start_ollama,
)
from youtube_transcript.config import load_config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def ensure_models_ready(transcript_model: str, validator_model: str):
    if not check_ollama_running():
        print("Ollama server not running. Starting...")
        start_ollama()
        time.sleep(3)

        if not check_ollama_running():
            print("Error: Could not connect to Ollama server")
            sys.exit(1)
    else:
        print("Ollama server is already running")

    for label, model_name in (
        ("transcript", transcript_model),
        ("validator", validator_model),
    ):
        if check_model_pulled(model_name):
            print(f"{label} model {model_name} is already pulled locally")
            continue

        print(f"{label} model {model_name} is not pulled. Pulling...")

        if not pull_model(model_name):
            print(f"Warning: Failed to pull {label} model {model_name}")


def main():
    config = load_config()

    transcript_model = config["models"]["transcript"]
    validator_model = config["models"]["validator"]
    config_url = config.get("youtube_url") or ""

    parser = argparse.ArgumentParser(description="Launch NotesMaker using config.yaml")
    parser.add_argument("url", nargs="?", help="YouTube URL (overrides config.yaml)")
    parser.add_argument(
        "--language",
        "-l",
        default="en",
        choices=["en", "hi", "bn"],
        help="Language code (default: en)",
    )
    parser.add_argument(
        "--no-translate", action="store_true", help="Disable translation"
    )
    parser.add_argument("--no-validate", action="store_true", help="Disable validation")
    parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Output directory (default: output)",
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check config and models"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("NOTES MAKER")
    print("=" * 60)
    print(f"\nConfig file: {config.get('_path', 'config.yaml')}")

    url = args.url or config_url

    print(f"YouTube URL: {url or '(not set - interactive mode)'}")
    print(f"Transcript model: {transcript_model}")
    print(f"Validator model: {validator_model}")

    print("\nChecking locally pulled models...\n")

    ensure_models_ready(transcript_model, validator_model)

    if args.check_only:
        print("\nCheck complete. Nothing was started.")
        return

    print("\nModels are ready. Starting start.py...\n")

    cmd = [sys.executable, os.path.join(PROJECT_ROOT, "start.py")]

    if url:
        cmd.append(url)

    cmd.extend(
        [
            "--language",
            args.language,
            "--output-dir",
            args.output_dir,
            "--skip-ollama",
        ]
    )

    if args.no_translate:
        cmd.append("--no-translate")

    if args.no_validate:
        cmd.append("--no-validate")

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
