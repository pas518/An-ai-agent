@echo off
title AI File Processing Agent
color 0A
echo.
echo ========================================
echo   AI File Processing Agent
echo   Starting Server...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Dependencies not found. Installing...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

echo Starting AI Agent Server...
echo.
echo Server will be available at: http://127.0.0.1:5000
echo Browser will open automatically...
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python app.py

pause

