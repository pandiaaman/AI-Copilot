# Test script to verify individual components
Write-Host "🧪 Testing MediaCentral CTMS Chatbot Components..." -ForegroundColor Blue
Write-Host ""

# Test 1: Environment checks
Write-Host "📋 Environment Checks:" -ForegroundColor Magenta

# Check Python
try {
    $pythonVersion = python3 --version 2>$null
    if (-not $pythonVersion) {
        $pythonVersion = python --version 2>$null
        $pythonCmd = "python"
    } else {
        $pythonCmd = "python3"
    }
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

# Check Node.js
try {
    $nodeVersion = node --version 2>$null
    $npmVersion = npm --version 2>$null
    Write-Host "✅ Node.js: $nodeVersion, npm: $npmVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Node.js not found" -ForegroundColor Red
}

# Test 2: Check required files
Write-Host ""
Write-Host "📁 File Structure Check:" -ForegroundColor Magenta

$requiredFiles = @(
    ".env",
    "requirements.txt",
    "fastapi app/app-improved.py",
    "react-frontend/ctms-chat-frontend/package.json"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (missing)" -ForegroundColor Red
    }
}

# Test 3: Virtual Environment
Write-Host ""
Write-Host "🐍 Virtual Environment Check:" -ForegroundColor Magenta

if (Test-Path "venv") {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
    
    # Check if uvicorn is installed
    try {
        & python -m pip show uvicorn >$null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ uvicorn installed" -ForegroundColor Green
        } else {
            Write-Host "⚠️  uvicorn not installed" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Unable to check uvicorn" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Virtual environment not found" -ForegroundColor Red
}

# Test 4: Port availability
Write-Host ""
Write-Host "🌐 Port Availability Check:" -ForegroundColor Magenta

# Check port 8000
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "⚠️  Port 8000 is in use" -ForegroundColor Yellow
} catch {
    Write-Host "✅ Port 8000 available" -ForegroundColor Green
}

# Check port 3000
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "⚠️  Port 3000 is in use" -ForegroundColor Yellow
} catch {
    Write-Host "✅ Port 3000 available" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎯 Test Summary Complete!" -ForegroundColor Blue
Write-Host "If all checks pass, you can run: .\start.ps1" -ForegroundColor Cyan