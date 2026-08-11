import argparse
import os
import subprocess
import sys
import time

import requests

from youtube_transcript.config import ConfigError, load_config

OLLAMA_HOST = "http://localhost:11434"


def check_ollama_running() -> bool:
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def start_ollama() -> subprocess.Popen:
    print("Starting Ollama server...")

    try:
        if sys.platform == "win32":
            process = subprocess.Popen(
                ["ollama", "serve"],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        for _ in range(30):
            time.sleep(1)

            if check_ollama_running():
                print("Ollama server started successfully")
                return process

        print("Warning: Ollama server may not be fully ready")
        return process
    except FileNotFoundError:
        print(
            "Error: 'ollama' command not found. "
            "Please install Ollama from https://ollama.com/download"
        )
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        sys.exit(1)


def check_model_pulled(model_name: str) -> bool:
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)

        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(m["name"].startswith(model_name.split(":")[0]) for m in models)
    except Exception:
        pass

    return False


def pull_model(model_name: str) -> bool:
    print(f"Pulling model: {model_name}...")

    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print(f"Model {model_name} pulled successfully")
            return True

        print(f"Error pulling model: {result.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("Model pull timed out")
        return False
    except Exception as e:
        print(f"Error pulling model: {e}")
        return False


def ensure_ollama_ready(
    transcript_model: str,
    validator_model: str,
):
    if not check_ollama_running():
        print("Ollama server not running. Starting...")
        start_ollama()
        time.sleep(3)

        if not check_ollama_running():
            print("Error: Could not connect to Ollama server")
            sys.exit(1)
    else:
        print("Ollama server is already running")

    if not check_model_pulled(transcript_model):
        print(f"Model {transcript_model} not found. Pulling...")

        if not pull_model(transcript_model):
            print("Warning: Could not pull model. Translation may fail.")
    else:
        print(f"Model {transcript_model} already available")

    if validator_model != transcript_model and not check_model_pulled(validator_model):
        print(f"Validator model {validator_model} not found. Pulling...")

        if not pull_model(validator_model):
            print("Warning: Could not pull validator model.")
    elif validator_model != transcript_model:
        print(f"Validator model {validator_model} already available")


def main():
    try:
        config = load_config()
    except ConfigError as error:
        print(f"Config error: {error}")
        sys.exit(1)

    transcript_model = config.transcript_model
    validator_model = config.validator_model
    config_url = config.youtube_url

    parser = argparse.ArgumentParser(
        description="NotesMaker YouTube Transcript Fetcher"
    )
    parser.add_argument("url", nargs="?", help="YouTube URL")
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
    parser.add_argument("--skip-ollama", action="store_true", help="Skip Ollama setup")

    args = parser.parse_args()

    if not args.skip_ollama:
        ensure_ollama_ready(transcript_model, validator_model)

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from youtube_transcript.run import run

    url = args.url or config_url

    if url:
        run(
            url=url,
            language=args.language,
            translate=not args.no_translate,
            validate=not args.no_validate,
            output_dir=args.output_dir,
        )


if __name__ == "__main__":
    main()
