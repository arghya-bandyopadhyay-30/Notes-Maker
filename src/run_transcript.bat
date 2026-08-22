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

"%PY_EXE%" launcher.py %*

echo.
echo ============================================
echo Done.
echo ============================================
echo.

pause
