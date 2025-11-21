# Stop script for MediaCentral CTMS Chatbot
Write-Host "🛑 Stopping MediaCentral CTMS Chatbot Services..." -ForegroundColor Red

# Stop all PowerShell jobs
$jobs = Get-Job
if ($jobs) {
    Write-Host "Stopping background jobs..." -ForegroundColor Yellow
    $jobs | Stop-Job
    $jobs | Remove-Job
    Write-Host "✅ All background jobs stopped" -ForegroundColor Green
} else {
    Write-Host "No background jobs found" -ForegroundColor Yellow
}

# Kill any remaining processes on ports 8080 and 3000
Write-Host "Checking for processes on ports 8080 and 3000..." -ForegroundColor Yellow

# For Windows
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    try {
        $proc8080 = Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object {
            (Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue).OwningProcess -contains $_.Id
        }
        if ($proc8080) {
            $proc8080 | Stop-Process -Force
            Write-Host "✅ Stopped FastAPI process on port 8080" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $proc3000 = Get-Process -Name "node*" -ErrorAction SilentlyContinue | Where-Object {
            (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue).OwningProcess -contains $_.Id
        }
        if ($proc3000) {
            $proc3000 | Stop-Process -Force
            Write-Host "✅ Stopped React process on port 3000" -ForegroundColor Green
        }
    } catch {}
} else {
    # For macOS/Linux
    try {
        $proc8080 = lsof -ti:8080 2>/dev/null
        if ($proc8080) {
            kill -9 $proc8080
            Write-Host "✅ Stopped process on port 8080" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $proc3000 = lsof -ti:3000 2>/dev/null
        if ($proc3000) {
            kill -9 $proc3000
            Write-Host "✅ Stopped process on port 3000" -ForegroundColor Green
        }
    } catch {}
}

Write-Host "🎉 All services stopped successfully!" -ForegroundColor Green