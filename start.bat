@echo off
REM Quick start script for Overlay Annotator (Windows)

echo ==================================================
echo Overlay Annotator v2 - Quick Start
echo ==================================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed

REM Run tests
echo.
echo Running quick tests...
python test_quick.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Tests failed
    pause
    exit /b 1
)

REM Start application
echo.
echo ==================================================
echo Starting Overlay Annotator...
echo ==================================================
echo.
echo Press Ctrl+Alt+S to capture screen region
echo.
python -m app.main

pause
