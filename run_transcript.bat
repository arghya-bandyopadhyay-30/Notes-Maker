@echo off
REM NotesMaker YouTube Transcript Fetcher - Windows Batch Script
REM This script starts Ollama, pulls required models, and runs the transcript fetcher

echo ============================================
echo NotesMaker YouTube Transcript Fetcher
echo ============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.12+
    exit /b 1
)

REM Check if Ollama is installed
where ollama >nul 2>&1
if errorlevel 1 (
    echo Error: Ollama not found. Please install from https://ollama.com/download
    exit /b 1
)

REM Start Ollama server in background if not running
echo Checking Ollama server...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Starting Ollama server...
    start /B ollama serve
    echo Waiting for Ollama to be ready...
    timeout /t 5 >nul
    
    REM Wait for server to be ready
    :wait_ollama
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 (
        timeout /t 2 >nul
        goto wait_ollama
    )
    echo Ollama server started successfully.
) else (
    echo Ollama server is already running.
)

REM Pull required models
echo Checking for required models...
curl -s http://localhost:11434/api/tags | findstr /I "llama3.2:3b" >nul
if errorlevel 1 (
    echo Pulling model llama3.2:3b (this may take a while)...
    ollama pull llama3.2:3b
    if errorlevel 1 (
        echo Warning: Failed to pull model. Translation may not work.
    ) else (
        echo Model pulled successfully.
    )
) else (
    echo Model llama3.2:3b already available.
)

echo.
echo ============================================
echo Setup complete. Starting transcript fetcher...
echo ============================================
echo.

REM Run the transcript fetcher
if "%~1"=="" (
    echo Running in interactive mode...
    python -m youtube_transcript.run
) else (
    echo Running with URL: %~1
    python -m youtube_transcript.run "%~1" %~2 %~3 %~4 %~5
)

echo.
echo Done.
pause