#!/bin/bash
# Enhanced MediaCentral CTMS Chatbot Startup Script for Unix/macOS
set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${CYAN}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${BLUE}🔧 $1${NC}"; }

# Header
clear
echo -e "${BLUE}🚀 MediaCentral CTMS Chatbot Startup Script${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "Working directory: $SCRIPT_DIR"

# Check if .env file exists
if [ ! -f ".env" ]; then
    log_error ".env file not found! Please ensure .env file exists in the root directory."
    exit 1
fi
log_success ".env file found"

# Check Python
log_step "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version)
    log_success "Found Python: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version)
    log_success "Found Python: $PYTHON_VERSION"
else
    log_error "Python not found! Please install Python 3.8 or higher."
    exit 1
fi

# Setup virtual environment
log_step "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    log_info "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    log_success "Virtual environment created"
else
    log_info "Virtual environment already exists"
fi

# Activate virtual environment
log_step "Activating virtual environment..."
source venv/bin/activate
log_success "Virtual environment activated"

# Install Python dependencies
log_step "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
log_success "Python dependencies installed"

# Check Node.js
log_step "Checking Node.js installation..."
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    NODE_VERSION=$(node --version)
    NPM_VERSION=$(npm --version)
    log_success "Found Node.js: $NODE_VERSION, npm: $NPM_VERSION"
else
    log_error "Node.js not found! Please install Node.js 16 or higher."
    exit 1
fi

# Setup React frontend
FRONTEND_DIR="react-frontend/ctms-chat-frontend"
if [ -d "$FRONTEND_DIR" ]; then
    log_step "Installing React dependencies..."
    cd "$FRONTEND_DIR"
    npm install
    log_success "React dependencies installed"
    cd "$SCRIPT_DIR"
else
    log_warning "React frontend directory not found at: $FRONTEND_DIR"
fi

# Start services
log_step "Starting services..."

# Create logs directory
mkdir -p logs

# Start FastAPI backend
log_info "Starting FastAPI backend..."
cd "fastapi app"
nohup python -m uvicorn app-improved:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd "$SCRIPT_DIR"
log_success "FastAPI backend started (PID: $BACKEND_PID)"

# Start React frontend
if [ -d "$FRONTEND_DIR" ]; then
    log_info "Starting React frontend..."
    cd "$FRONTEND_DIR"
    nohup npm start > ../../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../../logs/frontend.pid
    cd "$SCRIPT_DIR"
    log_success "React frontend started (PID: $FRONTEND_PID)"
fi

# Wait for services to start
log_step "Waiting for services to initialize..."
sleep 10

# Check services
log_step "Checking service status..."

# Check FastAPI
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    log_success "FastAPI backend is running at http://localhost:8000"
    log_success "API Documentation available at http://localhost:8000/docs"
else
    log_warning "FastAPI backend may still be starting..."
fi

# Check React
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    log_success "React frontend is running at http://localhost:3000"
else
    log_warning "React frontend may still be starting..."
fi

# Final status
echo ""
echo -e "${GREEN}🎉 Application Startup Complete!${NC}"
echo -e "${GREEN}=======================================${NC}"
log_success "Backend API: http://localhost:8000"
log_success "Frontend UI: http://localhost:3000"
log_success "API Docs: http://localhost:8000/docs"
echo ""
log_info "Backend PID: $BACKEND_PID (logged in logs/backend.pid)"
if [ ! -z "$FRONTEND_PID" ]; then
    log_info "Frontend PID: $FRONTEND_PID (logged in logs/frontend.pid)"
fi
echo ""
log_warning "To stop services, run: ./stop.sh"
echo ""

# Optional: Open browser (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    read -p "Open browser to frontend? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "http://localhost:3000"
    fi
fi