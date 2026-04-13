@echo off
REM Turbo Financials Form Handler - Startup Script for Windows

echo.
echo =========================================
echo    Turbo Financials Form Handler
echo    Starting Flask Application
echo =========================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if venv exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Clear any existing logs
if exist "logs" (
    echo Clearing old logs...
    del /q logs\*.log 2>nul
)

REM Run the Flask application
echo.
echo =========================================
echo    Application Starting...
echo =========================================
echo.
echo Home Page:      http://localhost:5000/
echo Admin Panel:    http://localhost:5000/admin/summary
echo.
echo Press CTRL+C to stop the server
echo.

python app.py

pause
