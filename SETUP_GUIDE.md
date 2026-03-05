# MediaCentral CTMS Chatbot - Complete Setup Guide

This guide provides step-by-step instructions to set up the MediaCentral CTMS Chatbot application on a new machine.

## 📋 Prerequisites

Before starting, ensure you have the following installed on your machine:

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://python.org/downloads/
   - Verify installation: `python3 --version` or `python --version`

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version` and `npm --version`

3. **Git**
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

### Platform-Specific Installation Commands

**macOS (using Homebrew):**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required software
brew install python3 node git
```

**Windows:**
```powershell
# Using Chocolatey (install Chocolatey first from chocolatey.org)
choco install python3 nodejs git

# Or download and install manually from official websites
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm git
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install python3 python3-pip nodejs npm git
```

## 🔑 Required API Keys

You'll need to obtain the following API keys before setting up the application:

### 1. OpenAI API Key
- **Purpose**: Powers the ChatGPT functionality
- **How to get**:
  1. Visit: https://platform.openai.com/
  2. Create an account or sign in
  3. Go to API Keys section
  4. Create a new secret key
  5. Copy the key (starts with `sk-...`)

### 2. Pinecone API Key
- **Purpose**: Vector database for document embeddings
- **How to get**:
  1. Visit: https://www.pinecone.io/
  2. Create an account or sign in
  3. Go to API Keys section
  4. Copy your API key (starts with `pcsk_...`)

### 3. Pinecone Index Names (if existing)
- **Purpose**: Names of your vector databases
- **Note**: If you don't have existing indexes, new ones will be created
- **Required indexes**:
  - `INDEX_NAME_PDF`: For PDF documents
  - `INDEX_NAME_ALL_TYPES`: For all document types
  - `INDEX_NAME_LARGE`: For large documents

## 📁 Project Setup

### Step 1: Clone or Download the Project

**Option A: Clone from Git (if available)**
```bash
git clone <repository-url>
cd AvidChatbot
```

**Option B: Manual Setup**
```bash
# Create project directory
mkdir MediaCentral-CTMS-Chatbot
cd MediaCentral-CTMS-Chatbot

# You'll need to copy all project files here
```

### Step 2: Verify Project Structure

Ensure your project has this structure:
```
MediaCentral-CTMS-Chatbot/
├── .env                              # API keys (you'll create this)
├── requirements.txt                  # Python dependencies
├── start.sh                         # Startup script (Unix/macOS)
├── start.ps1                        # Startup script (PowerShell)
├── start.bat                        # Startup script (Windows)
├── stop.sh                          # Stop script (Unix/macOS)  
├── stop.ps1                         # Stop script (PowerShell)
├── fastapi app/
│   ├── app-improved.py              # Enhanced FastAPI backend
│   └── app.py                       # Basic FastAPI backend
├── react-frontend/
│   └── ctms-chat-frontend/
│       ├── package.json             # React dependencies
│       ├── public/
│       └── src/
├── alltypes/                        # Document processing scripts
└── pdf/                            # PDF processing scripts
```

## ⚙️ Environment Configuration

### Step 3: Create Environment File

Create a `.env` file in the project root directory:

```bash
# Create the .env file
touch .env
```

Add the following content to `.env` (replace with your actual keys):

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Pinecone Configuration  
PINECONE_API_KEY=pcsk_your-pinecone-key-here

# Pinecone Index Names (modify as needed)
INDEX_NAME_PDF=ctms-pdf-index
INDEX_NAME_ALL_TYPES=ctms-alltypes-index
INDEX_NAME_LARGE=ctms-large-index

# Optional: Redis Configuration (for caching)
# REDIS_URL=redis://localhost:6379
# REDIS_PASSWORD=your-redis-password
```

### Step 4: Set File Permissions (Unix/macOS only)

Make the startup scripts executable:

```bash
chmod +x start.sh stop.sh
```

## 🚀 Installation & Startup

### Automated Setup (Recommended)

The project includes automated startup scripts that handle everything:

**For macOS/Linux:**
```bash
./start.sh
```

**For Windows (PowerShell):**
```powershell
.\start.ps1
```

**For Windows (Command Prompt):**
```cmd
start.bat
```

### What the Startup Scripts Do:

1. ✅ **Environment Check**: Verify Python and Node.js installation
2. ✅ **Virtual Environment**: Create and activate Python virtual environment
3. ✅ **Dependencies**: Install all Python packages from `requirements.txt`
4. ✅ **React Setup**: Install React dependencies with `npm install`
5. ✅ **Service Launch**: Start both backend (port 8000) and frontend (port 3000)
6. ✅ **Health Check**: Verify services are running correctly

## 🔧 Manual Setup (Alternative)

If you prefer manual setup or the automated scripts fail:

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 3: Install React Dependencies

```bash
cd react-frontend/ctms-chat-frontend
npm install
cd ../..
```

### Step 4: Start Backend Service

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI backend
cd "fastapi app"
python -m uvicorn app-improved:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Start Frontend Service (in new terminal)

```bash
cd react-frontend/ctms-chat-frontend
npm start
```

## 🌐 Access the Application

After successful startup:

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📊 Verification Steps

### 1. Check Services are Running

```bash
# Check backend
curl http://localhost:8000/health

# Check frontend (should return HTML)
curl http://localhost:3000
```

### 2. Test Basic Functionality

1. Open http://localhost:3000 in your browser
2. You should see the chat interface
3. Send a test message: "What is MediaCentral?"
4. Verify you get a response from the chatbot

### 3. Check API Documentation

1. Open http://localhost:8000/docs
2. You should see the FastAPI Swagger documentation
3. Try the `/health` endpoint to test API functionality

## 🛑 Stopping the Application

### Using Stop Scripts

**macOS/Linux:**
```bash
./stop.sh
```

**Windows (PowerShell):**
```powershell
.\stop.ps1
```

### Manual Stop

```bash
# Find and kill processes on specific ports
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
```bash
# Check if Python is installed
python3 --version
# or
python --version

# If not found, install Python 3.8+
```

#### 2. Node.js Not Found
```bash
# Check if Node.js is installed
node --version
npm --version

# If not found, install Node.js 16+
```

#### 3. Permission Denied (macOS/Linux)
```bash
chmod +x start.sh stop.sh
```

#### 4. Port Already in Use
```bash
# Kill existing processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

#### 5. Virtual Environment Issues
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 6. Missing Dependencies
```bash
# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt

cd react-frontend/ctms-chat-frontend
npm install
```

#### 7. API Key Issues
- Verify `.env` file exists in project root
- Check API keys are correctly formatted
- Ensure no extra spaces or quotes around keys
- Test API keys independently:
  ```bash
  # Test OpenAI key
  curl -H "Authorization: Bearer YOUR_OPENAI_KEY" \
       https://api.openai.com/v1/models
  ```

#### 8. Pinecone Connection Issues
- Verify Pinecone API key is correct
- Check index names exist or will be created
- Ensure network connection to Pinecone services

### Log Files

Check these locations for detailed error messages:

- **Backend logs**: `logs/backend.log`
- **Frontend logs**: `logs/frontend.log`
- **Terminal output**: Real-time error messages during startup

## 📚 Additional Configuration

### Optional: Redis Setup (for caching)

If you want to enable caching:

1. **Install Redis**:
   ```bash
   # macOS
   brew install redis
   
   # Ubuntu
   sudo apt install redis-server
   
   # Windows (via Chocolatey)
   choco install redis-64
   ```

2. **Start Redis**:
   ```bash
   redis-server
   ```

3. **Update .env**:
   ```env
   REDIS_URL=redis://localhost:6379
   ```

### Optional: Custom Pinecone Indexes

To create custom indexes:

1. Log into Pinecone dashboard
2. Create new indexes with these specifications:
   - **Dimension**: 384 (for all-MiniLM-L6-v2 model)
   - **Metric**: Cosine similarity
   - **Environment**: Choose based on your plan

## 🎯 Quick Start Checklist

Use this checklist to verify setup on a new machine:

- [ ] Python 3.8+ installed and verified
- [ ] Node.js 16+ installed and verified
- [ ] Git installed (if cloning repository)
- [ ] Project files copied/cloned to local machine
- [ ] `.env` file created with valid API keys
- [ ] Script permissions set (Unix/macOS only)
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] React dependencies installed
- [ ] Backend started successfully (port 8000)
- [ ] Frontend started successfully (port 3000)
- [ ] Health check endpoints responding
- [ ] Chat interface accessible and functional

## 📞 Support

If you encounter issues not covered in this guide:

1. **Check logs**: Review terminal output and log files
2. **Verify prerequisites**: Ensure all required software is installed
3. **Check API keys**: Verify all keys are correct and active
4. **Review permissions**: Ensure proper file permissions
5. **Test connectivity**: Verify internet connection for API calls

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment variables**: Use proper environment variable management
2. **Process management**: Use PM2, systemd, or Docker
3. **Reverse proxy**: Use nginx for production routing
4. **SSL certificates**: Implement HTTPS
5. **Monitoring**: Add application monitoring and logging
6. **Security**: Review and implement security best practices

---

**Setup Guide Version**: 1.0  
**Created**: March 6, 2026  
**Application**: MediaCentral CTMS Chatbot