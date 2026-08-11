@echo off
setlocal

echo ============================================
echo NotesMaker YouTube Transcript Fetcher
echo ============================================
echo.

set "PY_EXE=python"

if exist ".venv\Scripts\python.exe" (
    set "PY_EXE=%~dp0.venv\Scripts\python.exe"
)

"%PY_EXE%" --version >nul 2>&1

if errorlevel 1 (
    echo Error: Python not found.
    echo Please install Python 3.12 or newer.
    exit /b 1
)

echo Python found.
"%PY_EXE%" --version
echo.

set "OLLAMA_EXE="

where ollama >nul 2>&1

if not errorlevel 1 (
    set "OLLAMA_EXE=ollama"
) else if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
    set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe"
) else if exist "%PROGRAMFILES%\Ollama\ollama.exe" (
    set "OLLAMA_EXE=%PROGRAMFILES%\Ollama\ollama.exe"
) else if exist "%PROGRAMFILES(x86)%\Ollama\ollama.exe" (
    set "OLLAMA_EXE=%PROGRAMFILES(x86)%\Ollama\ollama.exe"
) else (
    echo Error: Ollama not found.
    echo Install Ollama from:
    echo https://ollama.com/download
    exit /b 1
)

echo Found Ollama at:
echo %OLLAMA_EXE%
echo.

echo Checking Ollama server...

curl -s http://localhost:11434/api/tags >nul 2>&1

if errorlevel 1 (
    echo Ollama server is not running.
    echo Starting Ollama server...

    if "%OLLAMA_EXE%"=="ollama" (
        start "" /B ollama serve
    ) else (
        start "" /B "%OLLAMA_EXE%" serve
    )

    echo Waiting for Ollama to start...

    :wait_ollama
    timeout /t 2 /nobreak >nul

    curl -s http://localhost:11434/api/tags >nul 2>&1

    if errorlevel 1 (
        goto wait_ollama
    )

    echo Ollama server started successfully.
) else (
    echo Ollama server is already running.
)

echo.

echo Checking for required model: llama3.2:3b

"%OLLAMA_EXE%" list 2>nul | findstr /B /C:"llama3.2:3b" >nul

if errorlevel 1 (
    echo Model not found.
    echo Pulling llama3.2:3b...
    echo This may take a while.
    echo.

    "%OLLAMA_EXE%" pull llama3.2:3b

    if errorlevel 1 (
        echo.
        echo WARNING: Failed to pull llama3.2:3b.
        echo.
        exit /b 1
    )

    echo.
    echo Model pulled successfully.
) else (
    echo Model llama3.2:3b is already available.
)

echo.
echo ============================================
echo Setup complete. Starting transcript fetcher...
echo ============================================
echo.

if "%~1"=="" (
    echo Running in interactive mode...
    "%PY_EXE%" -m youtube_transcript.run
) else (
    echo Running with URL:
    echo %~1
    echo.

    "%PY_EXE%" -m youtube_transcript.run "%~1" %~2 %~3 %~4 %~5
)

echo.
echo ============================================
echo Done.
echo ============================================
echo.

pause
