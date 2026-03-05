# Quick Setup Checklist - MediaCentral CTMS Chatbot

## 📋 Pre-Installation Requirements

### Software Installation
- [ ] **Python 3.8+** installed (`python3 --version`)
- [ ] **Node.js 16+** installed (`node --version`)
- [ ] **npm** available (`npm --version`)
- [ ] **Git** installed (`git --version`)

### API Keys Required
- [ ] **OpenAI API Key** (starts with `sk-proj-` or `sk-`)
- [ ] **Pinecone API Key** (starts with `pcsk_`)
- [ ] **Pinecone Index Names** (optional, can be created)

## 🔧 Setup Steps

### 1. Project Setup
- [ ] Project files copied to target machine
- [ ] Navigate to project directory
- [ ] Verify project structure (see SETUP_GUIDE.md)

### 2. Environment Configuration
- [ ] Create `.env` file in project root
- [ ] Add OpenAI API key to `.env`
- [ ] Add Pinecone API key to `.env`
- [ ] Add index names to `.env`
- [ ] Set script permissions: `chmod +x start.sh stop.sh` (Unix/macOS)

### 3. Quick Start (Automated)
- [ ] Run startup script: `./start.sh` or `.\start.ps1`
- [ ] Wait for setup completion (may take 2-3 minutes)
- [ ] Verify both services started successfully

### 4. Manual Verification
- [ ] Check backend: http://localhost:8000/health
- [ ] Check frontend: http://localhost:3000
- [ ] Test API docs: http://localhost:8000/docs
- [ ] Send test message in chat interface

## 🆘 If Automated Setup Fails

### Manual Setup Steps
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Install Python deps: `pip install -r requirements.txt`
- [ ] Install React deps: `cd react-frontend/ctms-chat-frontend && npm install`
- [ ] Start backend: `cd "fastapi app" && python -m uvicorn app-improved:app --reload --port 8000`
- [ ] Start frontend: `cd react-frontend/ctms-chat-frontend && npm start`

## ✅ Final Verification

### Service Status
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] No error messages in terminals
- [ ] Chat interface loads properly

### Functionality Test
- [ ] Send message: "What is MediaCentral CTMS?"
- [ ] Receive chatbot response
- [ ] Verify streaming responses work
- [ ] Check API documentation accessible

## 🛑 Stopping Services

- [ ] Run stop script: `./stop.sh` or `.\stop.ps1`
- [ ] OR manually kill processes: `lsof -ti:8000 | xargs kill -9`

## 📝 Notes

- **Setup time**: 5-10 minutes (first time)
- **Startup time**: 30-60 seconds (subsequent runs)
- **Required disk space**: ~500MB (with dependencies)
- **Memory usage**: ~1GB (both services running)

## 🔍 Common Issues

- **Python not found**: Install Python 3.8+
- **Node.js not found**: Install Node.js 16+
- **Permission denied**: Run `chmod +x start.sh stop.sh`
- **Port in use**: Kill existing processes or restart machine
- **API errors**: Check API keys in `.env` file

---
✅ **Setup Complete!** Your MediaCentral CTMS Chatbot is ready to use.