#!/usr/bin/env bash
# NotesMaker YouTube Transcript Fetcher - Linux/macOS Shell Script
# This script starts Ollama, pulls required models, and runs the transcript fetcher

set -e

echo "============================================"
echo "NotesMaker YouTube Transcript Fetcher"
echo "============================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found. Please install Python 3.12+"
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama not found. Please install from https://ollama.com/download"
    exit 1
fi

# Start Ollama server in background if not running
echo "Checking Ollama server..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    echo "Waiting for Ollama to be ready..."
    sleep 3
    
    # Wait for server to be ready
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "Ollama server started successfully."
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Error: Could not start Ollama server"
        exit 1
    fi
else
    echo "Ollama server is already running."
fi

# Pull required models
echo "Checking for required models..."
if ! curl -s http://localhost:11434/api/tags | grep -qi "llama3.2:3b"; then
    echo "Pulling model llama3.2:3b (this may take a while)..."
    ollama pull llama3.2:3b
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to pull model. Translation may not work."
    else
        echo "Model pulled successfully."
    fi
else
    echo "Model llama3.2:3b already available."
fi

echo ""
echo "============================================"
echo "Setup complete. Starting transcript fetcher..."
echo "============================================"
echo ""

# Run the transcript fetcher
if [ $# -eq 0 ]; then
    echo "Running in interactive mode..."
    python3 -m youtube_transcript.run
else
    echo "Running with URL: $1"
    python3 -m youtube_transcript.run "$@"
fi

echo ""
echo "Done."