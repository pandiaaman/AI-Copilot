# MediaCentral CTMS Chatbot - Startup Scripts

This directory contains comprehensive startup scripts that automatically set up the environment and launch both the FastAPI backend and React frontend.

## 📁 Available Scripts

### Main Startup Scripts
- **`start.ps1`** - PowerShell script (Windows/macOS/Linux) ⭐ **Recommended**
- **`start.sh`** - Bash script (macOS/Linux)
- **`start.bat`** - Batch script (Windows fallback)

### Stop Scripts
- **`stop.ps1`** - PowerShell stop script
- **`stop.sh`** - Bash stop script

## 🚀 Quick Start

### Option 1: PowerShell (Recommended - Cross Platform)
```powershell
# Basic startup
.\start.ps1

# With options
.\start.ps1 -SkipInstall    # Skip dependency installation
.\start.ps1 -DevMode       # Run with continuous monitoring
.\start.ps1 -CleanStart    # Fresh installation (removes existing venv)
```

### Option 2: Bash (macOS/Linux)
```bash
# First time setup (make executable)
chmod +x start.sh stop.sh

# Start the application
./start.sh
```

### Option 3: Windows Batch
```cmd
start.bat
```

## ✨ What These Scripts Do

### 🔧 **Environment Setup**
1. ✅ Checks for Python 3.8+ and Node.js 16+
2. ✅ Creates/activates Python virtual environment
3. ✅ Installs all Python dependencies from `requirements.txt`
4. ✅ Installs React dependencies with `npm install`

### 🚀 **Service Launch**
1. ✅ Starts FastAPI backend on port 8000 with hot reload
2. ✅ Starts React development server on port 3000
3. ✅ Performs health checks to verify services are running
4. ✅ Shows all service URLs and status

### 📊 **Monitoring & Logs**
1. ✅ Creates `logs/` directory for service logs
2. ✅ Tracks process IDs for proper cleanup
3. ✅ Health check endpoints for service verification
4. ✅ Colored output for better user experience

## 🌐 Service URLs

After successful startup, you can access:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛑 Stopping Services

### PowerShell
```powershell
.\stop.ps1
```

### Bash
```bash
./stop.sh
```

### Manual Stop
If the stop scripts don't work, you can manually kill processes:
```bash
# Kill processes on specific ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

## ⚙️ Script Options

### PowerShell Script Parameters

| Parameter | Description |
|-----------|-------------|
| `-SkipInstall` | Skip dependency installation (faster startup if deps already installed) |
| `-DevMode` | Run in development mode with continuous monitoring |
| `-CleanStart` | Remove existing virtual environment and start fresh |

### Examples
```powershell
# Fast startup (skip dependency check)
.\start.ps1 -SkipInstall

# Clean installation
.\start.ps1 -CleanStart

# Development mode with monitoring
.\start.ps1 -DevMode
```

## 🔍 Troubleshooting

### Common Issues

**1. Python not found**
```bash
# Install Python 3.8+
# macOS: brew install python3
# Windows: Download from python.org
# Linux: sudo apt install python3 python3-pip
```

**2. Node.js not found**
```bash
# Install Node.js 16+
# macOS: brew install node
# Windows: Download from nodejs.org
# Linux: sudo apt install nodejs npm
```

**3. Permission denied (macOS/Linux)**
```bash
chmod +x start.sh stop.sh
```

**4. Port already in use**
```bash
# Kill existing processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**5. Virtual environment issues**
```powershell
# Clean start
.\start.ps1 -CleanStart
```

### Log Files
Check the `logs/` directory for detailed error messages:
- `logs/backend.log` - FastAPI backend logs
- `logs/frontend.log` - React frontend logs

## 📋 Prerequisites

### Required Software
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning)

### Required Files
- `.env` file with API keys (OpenAI, Pinecone)
- `requirements.txt` for Python dependencies
- `react-frontend/ctms-chat-frontend/package.json` for React dependencies

## 🎯 Features

### ✅ **Automated Setup**
- No manual virtual environment creation
- Automatic dependency resolution
- Cross-platform compatibility

### ✅ **Intelligent Checks**
- Validates all prerequisites
- Health checks for running services
- Proper error handling and reporting

### ✅ **User Experience**
- Colored output for better readability
- Progress indicators
- Optional browser opening
- Clean shutdown procedures

### ✅ **Development Friendly**
- Hot reload for both backend and frontend
- Separate log files for debugging
- Development mode with monitoring
- Easy service management

## 🔧 Advanced Usage

### Running with Custom Options
```powershell
# Skip dependencies and run in dev mode
.\start.ps1 -SkipInstall -DevMode

# Clean start with monitoring
.\start.ps1 -CleanStart -DevMode
```

### Checking Service Status
```bash
# Check if services are running
curl http://localhost:8000/health
curl http://localhost:3000
```

### Viewing Real-time Logs
```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs  
tail -f logs/frontend.log
```

---

## 🎉 Quick Test

1. **Run the startup script**:
   ```bash
   ./start.sh
   ```

2. **Verify services are running**:
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

3. **Test the chatbot**:
   - Open http://localhost:3000
   - Send a test message about MediaCentral CTMS

4. **Stop when done**:
   ```bash
   ./stop.sh
   ```

That's it! 🚀 Your MediaCentral CTMS Chatbot is ready to use!