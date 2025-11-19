@echo off
REM MediaCentral CTMS Chatbot Startup Script for Windows

echo Starting MediaCentral CTMS Chatbot...
echo.

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% == 0 (
    echo Using PowerShell script...
    powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
) else (
    echo PowerShell not available, using basic batch script...
    
    REM Basic batch implementation
    echo Setting up virtual environment...
    if not exist venv (
        python -m venv venv
    )
    
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
    
    echo Starting FastAPI backend...
    start /b cmd /c "cd /d "%~dp0fastapi app" && python -m uvicorn app-improved:app --reload"
    
    echo Starting React frontend...
    start /b cmd /c "cd /d "%~dp0react-frontend\ctms-chat-frontend" && npm start"
    
    echo.
    echo Services are starting...
    echo Backend: http://localhost:8000
    echo Frontend: http://localhost:3000
    echo.
    pause
)