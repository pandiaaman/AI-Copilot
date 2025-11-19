# Enhanced MediaCentral CTMS Chatbot Startup Script
# This script sets up the environment and starts both backend and frontend

param(
    [switch]$SkipInstall,  # Skip dependency installation
    [switch]$DevMode,      # Run in development mode with verbose output
    [switch]$CleanStart    # Clean install (remove existing venv)
)

# Set error handling
$ErrorActionPreference = "Stop"

# Color functions for better output
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Step { param($Message) Write-Host "🔧 $Message" -ForegroundColor Magenta }

# Header
Clear-Host
Write-Host "🚀 MediaCentral CTMS Chatbot Startup Script" -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue
Write-Host ""

try {
    # Get script directory
    $ScriptDir = $PSScriptRoot
    if (-not $ScriptDir) {
        $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    }
    
    Write-Info "Working directory: $ScriptDir"
    Set-Location $ScriptDir

    # Check if .env file exists
    if (-not (Test-Path ".env")) {
        Write-Error ".env file not found! Please ensure .env file exists in the root directory."
        exit 1
    }
    Write-Success ".env file found"

    # Step 1: Setup Python Virtual Environment
    Write-Step "Setting up Python virtual environment..."
    
    # Clean start if requested
    if ($CleanStart -and (Test-Path "venv")) {
        Write-Info "Removing existing virtual environment..."
        Remove-Item -Path "venv" -Recurse -Force
    }

    # Check if Python is available
    try {
        $pythonVersion = python3 --version 2>$null
        if (-not $pythonVersion) {
            $pythonVersion = python --version 2>$null
            $pythonCmd = "python"
        } else {
            $pythonCmd = "python3"
        }
        Write-Success "Found Python: $pythonVersion"
    }
    catch {
        Write-Error "Python not found! Please install Python 3.8 or higher."
        exit 1
    }

    # Create virtual environment if it doesn't exist
    if (-not (Test-Path "venv")) {
        Write-Step "Creating virtual environment..."
        & $pythonCmd -m venv venv
        Write-Success "Virtual environment created"
    } else {
        Write-Info "Virtual environment already exists"
    }

    # Activate virtual environment
    Write-Step "Activating virtual environment..."
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        $activateScript = "venv\Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            & $activateScript
        } else {
            Write-Warning "PowerShell activation script not found, using batch file..."
            & "venv\Scripts\activate.bat"
        }
    } else {
        # macOS/Linux
        $env:VIRTUAL_ENV = Join-Path $ScriptDir "venv"
        $env:PATH = Join-Path $env:VIRTUAL_ENV "bin" + [IO.Path]::PathSeparator + $env:PATH
    }
    Write-Success "Virtual environment activated"

    # Step 2: Install Python dependencies
    if (-not $SkipInstall) {
        Write-Step "Installing Python dependencies..."
        
        # Upgrade pip first
        Write-Info "Upgrading pip..."
        python -m pip install --upgrade pip

        # Install requirements
        if (Test-Path "requirements.txt") {
            Write-Info "Installing from requirements.txt..."
            python -m pip install -r requirements.txt
            Write-Success "Python dependencies installed"
        } else {
            Write-Warning "requirements.txt not found, installing core dependencies..."
            python -m pip install fastapi uvicorn langchain langchain-openai langchain-pinecone pinecone redis sentence-transformers scikit-learn python-dotenv
        }
    } else {
        Write-Info "Skipping dependency installation"
    }

    # Step 3: Check Node.js and npm
    Write-Step "Checking Node.js environment..."
    try {
        $nodeVersion = node --version 2>$null
        $npmVersion = npm --version 2>$null
        Write-Success "Found Node.js: $nodeVersion, npm: $npmVersion"
    }
    catch {
        Write-Error "Node.js not found! Please install Node.js 16 or higher."
        exit 1
    }

    # Step 4: Setup React frontend
    $frontendDir = "react-frontend\ctms-chat-frontend"
    if (Test-Path $frontendDir) {
        Write-Step "Setting up React frontend..."
        Set-Location $frontendDir
        
        if (-not $SkipInstall) {
            Write-Info "Installing npm dependencies..."
            npm install
            Write-Success "React dependencies installed"
        }
        
        Set-Location $ScriptDir
    } else {
        Write-Warning "React frontend directory not found at: $frontendDir"
    }

    # Step 5: Start services
    Write-Step "Starting services..."
    
    # Create output directories for logs
    if (-not (Test-Path "logs")) {
        New-Item -ItemType Directory -Path "logs" | Out-Null
    }

    Write-Info "Starting FastAPI backend..."
    
    # Start FastAPI backend in background
    $fastApiPath = "fastapi app"
    if (Test-Path $fastApiPath) {
        $backendJob = Start-Job -ScriptBlock {
            param($WorkingDir, $FastApiPath, $PythonPath)
            Set-Location $WorkingDir
            Set-Location $FastApiPath
            & $PythonPath -m uvicorn app-improved:app --reload --host 0.0.0.0 --port 8000
        } -ArgumentList $ScriptDir, $fastApiPath, (Get-Command python).Source
        
        Write-Success "FastAPI backend starting... (Job ID: $($backendJob.Id))"
    } else {
        Write-Error "FastAPI app directory not found!"
        exit 1
    }

    # Wait a moment for backend to start
    Start-Sleep -Seconds 3

    # Start React frontend
    if (Test-Path $frontendDir) {
        Write-Info "Starting React frontend..."
        
        $frontendJob = Start-Job -ScriptBlock {
            param($WorkingDir, $FrontendDir)
            Set-Location $WorkingDir
            Set-Location $FrontendDir
            npm start
        } -ArgumentList $ScriptDir, $frontendDir
        
        Write-Success "React frontend starting... (Job ID: $($frontendJob.Id))"
    }

    # Wait for services to initialize
    Write-Step "Waiting for services to start..."
    Start-Sleep -Seconds 5

    # Check service status
    Write-Step "Checking service status..."
    
    # Check FastAPI
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Success "FastAPI backend is running at http://localhost:8000"
        Write-Success "API Documentation available at http://localhost:8000/docs"
    }
    catch {
        Write-Warning "FastAPI backend may still be starting..."
    }

    # Check React (it takes longer to start)
    Start-Sleep -Seconds 10
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -ErrorAction Stop
        Write-Success "React frontend is running at http://localhost:3000"
    }
    catch {
        Write-Warning "React frontend may still be starting..."
    }

    # Final status
    Write-Host ""
    Write-Host "🎉 Application Startup Complete!" -ForegroundColor Green
    Write-Host "=" * 40 -ForegroundColor Green
    Write-Success "Backend API: http://localhost:8000"
    Write-Success "Frontend UI: http://localhost:3000"
    Write-Success "API Docs: http://localhost:8000/docs"
    Write-Host ""
    Write-Info "Backend Job ID: $($backendJob.Id)"
    if ($frontendJob) {
        Write-Info "Frontend Job ID: $($frontendJob.Id)"
    }
    Write-Host ""
    Write-Warning "To stop services, run: .\stop.ps1"
    Write-Host ""

    # Optional: Open browser
    $openBrowser = Read-Host "Open browser to frontend? (y/N)"
    if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
        Start-Process "http://localhost:3000"
    }

    # Keep script running and monitor jobs
    if ($DevMode) {
        Write-Host "Running in development mode. Press Ctrl+C to stop all services." -ForegroundColor Yellow
        Write-Host ""
        
        try {
            while ($true) {
                # Check job status
                $runningJobs = Get-Job | Where-Object { $_.State -eq "Running" }
                if ($runningJobs.Count -eq 0) {
                    Write-Warning "All services have stopped."
                    break
                }
                
                # Show any job output
                Get-Job | Receive-Job
                Start-Sleep -Seconds 2
            }
        }
        catch {
            Write-Info "Stopping all services..."
        }
        finally {
            Get-Job | Stop-Job
            Get-Job | Remove-Job
            Write-Success "All services stopped."
        }
    }

}
catch {
    Write-Error "An error occurred: $($_.Exception.Message)"
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    exit 1
}