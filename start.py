#!/usr/bin/env python3
"""
Startup script for NotesMaker YouTube Transcript Fetcher.
Handles Ollama setup (start service, pull model) and runs the transcript fetcher.
"""
import os
import sys
import subprocess
import time
import requests
import argparse


OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"
VALIDATOR_MODEL = "llama3.2:3b"


def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def start_ollama() -> subprocess.Popen:
    """Start Ollama server in background."""
    print("Starting Ollama server...")
    try:
        # On Windows, use CREATE_NEW_CONSOLE to run in background
        if sys.platform == "win32":
            process = subprocess.Popen(
                ["ollama", "serve"],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait for server to be ready
        for _ in range(30):
            time.sleep(1)
            if check_ollama_running():
                print("Ollama server started successfully")
                return process
        
        print("Warning: Ollama server may not be fully ready")
        return process
    except FileNotFoundError:
        print("Error: 'ollama' command not found. Please install Ollama from https://ollama.com/download")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        sys.exit(1)


def check_model_pulled(model_name: str) -> bool:
    """Check if model is already pulled."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(m["name"].startswith(model_name.split(":")[0]) for m in models)
    except Exception:
        pass
    return False


def pull_model(model_name: str) -> bool:
    """Pull model using ollama CLI."""
    print(f"Pulling model: {model_name}...")
    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"Model {model_name} pulled successfully")
            return True
        else:
            print(f"Error pulling model: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Model pull timed out")
        return False
    except Exception as e:
        print(f"Error pulling model: {e}")
        return False


def ensure_ollama_ready():
    """Ensure Ollama is running and required models are pulled."""
    # Check if Ollama is running
    if not check_ollama_running():
        print("Ollama server not running. Starting...")
        start_ollama()
        
        # Wait a bit more for full readiness
        time.sleep(3)
        if not check_ollama_running():
            print("Error: Could not connect to Ollama server")
            sys.exit(1)
    else:
        print("Ollama server is already running")
    
    # Check and pull main model
    if not check_model_pulled(MODEL_NAME):
        print(f"Model {MODEL_NAME} not found. Pulling...")
        if not pull_model(MODEL_NAME):
            print("Warning: Could not pull model. Translation may fail.")
    else:
        print(f"Model {MODEL_NAME} already available")
    
    # Check and pull validator model (if different)
    if VALIDATOR_MODEL != MODEL_NAME and not check_model_pulled(VALIDATOR_MODEL):
        print(f"Validator model {VALIDATOR_MODEL} not found. Pulling...")
        if not pull_model(VALIDATOR_MODEL):
            print("Warning: Could not pull validator model.")
    elif VALIDATOR_MODEL != MODEL_NAME:
        print(f"Validator model {VALIDATOR_MODEL} already available")


def main():
    parser = argparse.ArgumentParser(description="NotesMaker YouTube Transcript Fetcher")
    parser.add_argument("url", nargs="?", help="YouTube URL")
    parser.add_argument("--language", "-l", default="en", choices=["en", "hi", "bn"], help="Language code (default: en)")
    parser.add_argument("--no-translate", action="store_true", help="Disable translation")
    parser.add_argument("--no-validate", action="store_true", help="Disable validation")
    parser.add_argument("--output-dir", "-o", default="output", help="Output directory (default: output)")
    parser.add_argument("--skip-ollama", action="store_true", help="Skip Ollama setup")
    
    args = parser.parse_args()
    
    # Ensure Ollama is ready (unless skipped)
    if not args.skip_ollama:
        ensure_ollama_ready()
    
    # Import and run the transcript fetcher
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from youtube_transcript.run import run, interactive_mode
    
    if args.url:
        run(
            url=args.url,
            language=args.language,
            translate=not args.no_translate,
            validate=not args.no_validate,
            output_dir=args.output_dir
        )
    else:
        interactive_mode()


if __name__ == "__main__":
    main()