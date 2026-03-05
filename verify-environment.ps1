# Environment Verification Script for MediaCentral CTMS Chatbot (PowerShell)
# Run this script to check if your system meets all requirements

# Color functions
function Write-Section { param($Message) Write-Host "🔍 $Message" -ForegroundColor Blue }
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }

# Header
Clear-Host
Write-Host "🔍 MediaCentral CTMS Chatbot - Environment Verification" -ForegroundColor Blue
Write-Host "====================================================" -ForegroundColor Blue
Write-Host ""

# Track verification status
$script:Errors = 0
$script:Warnings = 0
$script:Successes = 0

# Function to update counters
function Update-Status {
    param($Status)
    switch ($Status) {
        "success" { $script:Successes++ }
        "error" { $script:Errors++ }
        "warning" { $script:Warnings++ }
    }
}

try {
    # 1. Check Operating System
    Write-Section "Operating System"
    $OSInfo = Get-WmiObject -Class Win32_OperatingSystem -ErrorAction SilentlyContinue
    
    if ($OSInfo) {
        Write-Info "Detected: $($OSInfo.Caption) $($OSInfo.Version)"
        Write-Success "Windows detected"
        Update-Status "success"
    } else {
        # Fallback for non-Windows or modern PowerShell
        $OS = [System.Environment]::OSVersion
        Write-Info "Detected: $($OS.Platform) $($OS.Version)"
        if ($OS.Platform -eq "Win32NT") {
            Write-Success "Windows detected"
            Update-Status "success"
        } else {
            Write-Success "Non-Windows OS detected"
            Update-Status "success"
        }
    }
    Write-Host ""

    # 2. Check Python Installation
    Write-Section "Python Installation"
    
    $pythonFound = $false
    $pythonCmd = ""
    
    try {
        $pythonVersion = python3 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "python3"
            $pythonFound = $true
            Write-Success "Python3 found: $pythonVersion"
            
            # Check version compatibility
            $versionNumber = $pythonVersion -replace "Python ", ""
            $versionParts = $versionNumber.Split('.')
            $major = [int]$versionParts[0]
            $minor = [int]$versionParts[1]
            
            if ($major -ge 3 -and $minor -ge 8) {
                Write-Success "Python version compatible (3.8+ required)"
                Update-Status "success"
            } else {
                Write-Error "Python version too old. Need 3.8+, found $versionNumber"
                Update-Status "error"
            }
        }
    } catch {}
    
    if (-not $pythonFound) {
        try {
            $pythonVersion = python --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = "python"
                $pythonFound = $true
                Write-Warning "Using 'python' command: $pythonVersion"
                Update-Status "warning"
            }
        } catch {}
    }
    
    if (-not $pythonFound) {
        Write-Error "Python not found! Install Python 3.8+ from https://python.org"
        Update-Status "error"
    }

    # Check pip
    try {
        $pipCheck = & $pythonCmd -m pip --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "pip found"
            Update-Status "success"
        } else {
            Write-Error "pip not found! Install pip for package management"
            Update-Status "error"
        }
    } catch {
        Write-Error "pip not found! Install pip for package management"
        Update-Status "error"
    }

    # Check virtual environment support
    try {
        $venvCheck = & $pythonCmd -m venv --help 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Virtual environment support available"
            Update-Status "success"
        } else {
            Write-Error "Virtual environment (venv) not available"
            Update-Status "error"
        }
    } catch {
        Write-Error "Virtual environment (venv) not available"
        Update-Status "error"
    }
    Write-Host ""

    # 3. Check Node.js Installation
    Write-Section "Node.js Installation"
    
    try {
        $nodeVersion = node --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Node.js found: $nodeVersion"
            
            # Check version compatibility
            $versionNumber = $nodeVersion -replace "v", ""
            $major = [int]$versionNumber.Split('.')[0]
            
            if ($major -ge 16) {
                Write-Success "Node.js version compatible (16+ required)"
                Update-Status "success"
            } else {
                Write-Error "Node.js version too old. Need 16+, found $nodeVersion"
                Update-Status "error"
            }
        } else {
            Write-Error "Node.js not found! Install from https://nodejs.org"
            Update-Status "error"
        }
    } catch {
        Write-Error "Node.js not found! Install from https://nodejs.org"
        Update-Status "error"
    }

    # Check npm
    try {
        $npmVersion = npm --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "npm found: $npmVersion"
            Update-Status "success"
        } else {
            Write-Error "npm not found! Should be installed with Node.js"
            Update-Status "error"
        }
    } catch {
        Write-Error "npm not found! Should be installed with Node.js"
        Update-Status "error"
    }
    Write-Host ""

    # 4. Check Git Installation
    Write-Section "Git Installation"
    
    try {
        $gitVersion = git --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$gitVersion"
            Update-Status "success"
        } else {
            Write-Warning "Git not found (optional, needed only for cloning repositories)"
            Update-Status "warning"
        }
    } catch {
        Write-Warning "Git not found (optional, needed only for cloning repositories)"
        Update-Status "warning"
    }
    Write-Host ""

    # 5. Check Project Structure
    Write-Section "Project Structure"
    
    $requiredFiles = @(
        "requirements.txt",
        "fastapi app\app-improved.py",
        "react-frontend\ctms-chat-frontend\package.json"
    )
    
    $optionalFiles = @(
        ".env",
        "start.ps1",
        "start.sh",
        "start.bat",
        "stop.ps1"
    )

    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Success "Found: $file"
            Update-Status "success"
        } else {
            Write-Error "Missing required file: $file"
            Update-Status "error"
        }
    }

    foreach ($file in $optionalFiles) {
        if (Test-Path $file) {
            Write-Success "Found: $file"
            Update-Status "success"
        } else {
            Write-Warning "Optional file missing: $file"
            Update-Status "warning"
        }
    }
    Write-Host ""

    # 6. Check Environment Configuration
    Write-Section "Environment Configuration"
    
    if (Test-Path ".env") {
        Write-Success ".env file found"
        
        $envContent = Get-Content ".env"
        
        # Check OpenAI API Key
        $openaiLine = $envContent | Where-Object { $_ -match "OPENAI_API_KEY=" }
        if ($openaiLine) {
            $openaiKey = ($openaiLine -split "=", 2)[1]
            if ($openaiKey.Length -gt 10) {
                Write-Success "OpenAI API key configured"
                Update-Status "success"
            } else {
                Write-Error "OpenAI API key appears empty or invalid"
                Update-Status "error"
            }
        } else {
            Write-Error "OPENAI_API_KEY not found in .env"
            Update-Status "error"
        }
        
        # Check Pinecone API Key
        $pineconeLine = $envContent | Where-Object { $_ -match "PINECONE_API_KEY=" }
        if ($pineconeLine) {
            $pineconeKey = ($pineconeLine -split "=", 2)[1]
            if ($pineconeKey.Length -gt 10) {
                Write-Success "Pinecone API key configured"
                Update-Status "success"
            } else {
                Write-Error "Pinecone API key appears empty or invalid"
                Update-Status "error"
            }
        } else {
            Write-Error "PINECONE_API_KEY not found in .env"
            Update-Status "error"
        }
        
    } else {
        Write-Error ".env file not found! Create it with your API keys"
        Update-Status "error"
    }
    Write-Host ""

    # 7. Check Port Availability
    Write-Section "Port Availability"
    
    # Check port 8000 (Backend)
    $port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if (-not $port8000) {
        Write-Success "Port 8000 available for backend"
        Update-Status "success"
    } else {
        Write-Warning "Port 8000 is in use (may need to stop existing services)"
        Update-Status "warning"
    }

    # Check port 3000 (Frontend)
    $port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
    if (-not $port3000) {
        Write-Success "Port 3000 available for frontend"
        Update-Status "success"
    } else {
        Write-Warning "Port 3000 is in use (may need to stop existing services)"
        Update-Status "warning"
    }
    Write-Host ""

    # 8. Check Internet Connectivity
    Write-Section "Internet Connectivity"
    
    try {
        $ping = Test-Connection -ComputerName "google.com" -Count 1 -ErrorAction Stop
        Write-Success "Internet connection available"
        Update-Status "success"
    } catch {
        Write-Warning "Internet connection check failed (needed for API calls)"
        Update-Status "warning"
    }

    # Check API endpoints
    try {
        $response = Invoke-WebRequest -Uri "https://api.openai.com" -Method Head -TimeoutSec 5 -ErrorAction Stop
        Write-Success "OpenAI API endpoint reachable"
        Update-Status "success"
    } catch {
        Write-Warning "Cannot reach OpenAI API (check network/firewall)"
        Update-Status "warning"
    }
    Write-Host ""

    # Summary
    Write-Host "📊 Verification Summary" -ForegroundColor Blue
    Write-Host "=====================" -ForegroundColor Blue
    Write-Success "Successes: $($script:Successes)"
    Write-Warning "Warnings:  $($script:Warnings)"
    Write-Error "Errors:    $($script:Errors)"
    Write-Host ""

    # Final status
    if ($script:Errors -eq 0) {
        Write-Host "🎉 All critical requirements met! You can proceed with installation." -ForegroundColor Green
        Write-Info "Run '.\start.ps1' to start the application."
        exit 0
    } elseif ($script:Errors -le 2 -and $script:Warnings -gt 0) {
        Write-Host "⚠️  Minor issues detected but installation may work." -ForegroundColor Yellow
        Write-Info "Try running the startup script and check for errors."
        exit 1
    } else {
        Write-Host "❌ Critical issues found! Please resolve errors before proceeding." -ForegroundColor Red
        Write-Info "Refer to SETUP_GUIDE.md for detailed installation instructions."
        exit 2
    }

} catch {
    Write-Error "An error occurred during verification: $($_.Exception.Message)"
    exit 3
}