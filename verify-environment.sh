#!/bin/bash
# Environment Verification Script for MediaCentral CTMS Chatbot
# Run this script to check if your system meets all requirements

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
log_section() { echo -e "${BLUE}🔍 $1${NC}"; }

# Header
clear
echo -e "${BLUE}🔍 MediaCentral CTMS Chatbot - Environment Verification${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

# Track verification status
ERRORS=0
WARNINGS=0
SUCCESSES=0

# Function to update counters
update_status() {
    case $1 in
        "success") ((SUCCESSES++)) ;;
        "error") ((ERRORS++)) ;;
        "warning") ((WARNINGS++)) ;;
    esac
}

# 1. Check Operating System
log_section "Operating System"
OS_NAME=$(uname -s)
OS_VERSION=$(uname -r)
log_info "Detected: $OS_NAME $OS_VERSION"

if [[ "$OS_NAME" == "Darwin" ]]; then
    log_success "macOS detected"
    update_status "success"
elif [[ "$OS_NAME" == "Linux" ]]; then
    log_success "Linux detected"
    update_status "success"
else
    log_warning "Unsupported OS: $OS_NAME (script optimized for macOS/Linux)"
    update_status "warning"
fi
echo ""

# 2. Check Python Installation
log_section "Python Installation"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    PYTHON_CMD="python3"
    log_success "Python3 found: $PYTHON_VERSION"
    
    # Check version compatibility (3.8+)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [[ $PYTHON_MAJOR -ge 3 && $PYTHON_MINOR -ge 8 ]]; then
        log_success "Python version compatible (3.8+ required)"
        update_status "success"
    else
        log_error "Python version too old. Need 3.8+, found $PYTHON_VERSION"
        update_status "error"
    fi
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    PYTHON_CMD="python"
    log_warning "Using 'python' command: $PYTHON_VERSION"
    update_status "warning"
else
    log_error "Python not found! Install Python 3.8+ from https://python.org"
    update_status "error"
fi

# Check pip
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    log_success "pip found"
    update_status "success"
else
    log_error "pip not found! Install pip for package management"
    update_status "error"
fi

# Check virtual environment support
if $PYTHON_CMD -m venv --help &> /dev/null; then
    log_success "Virtual environment support available"
    update_status "success"
else
    log_error "Virtual environment (venv) not available"
    update_status "error"
fi
echo ""

# 3. Check Node.js Installation
log_section "Node.js Installation"

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    log_success "Node.js found: $NODE_VERSION"
    
    # Check version compatibility (16+)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    
    if [[ $NODE_MAJOR -ge 16 ]]; then
        log_success "Node.js version compatible (16+ required)"
        update_status "success"
    else
        log_error "Node.js version too old. Need 16+, found $NODE_VERSION"
        update_status "error"
    fi
else
    log_error "Node.js not found! Install from https://nodejs.org"
    update_status "error"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    log_success "npm found: $NPM_VERSION"
    update_status "success"
else
    log_error "npm not found! Should be installed with Node.js"
    update_status "error"
fi
echo ""

# 4. Check Git Installation
log_section "Git Installation"

if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    log_success "$GIT_VERSION"
    update_status "success"
else
    log_warning "Git not found (optional, needed only for cloning repositories)"
    update_status "warning"
fi
echo ""

# 5. Check Project Structure
log_section "Project Structure"

REQUIRED_FILES=(
    "requirements.txt"
    "fastapi app/app-improved.py"
    "react-frontend/ctms-chat-frontend/package.json"
)

OPTIONAL_FILES=(
    ".env"
    "start.sh"
    "start.ps1"
    "stop.sh"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        log_success "Found: $file"
        update_status "success"
    else
        log_error "Missing required file: $file"
        update_status "error"
    fi
done

for file in "${OPTIONAL_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        log_success "Found: $file"
        update_status "success"
    else
        log_warning "Optional file missing: $file"
        update_status "warning"
    fi
done
echo ""

# 6. Check Environment Configuration
log_section "Environment Configuration"

if [[ -f ".env" ]]; then
    log_success ".env file found"
    
    # Check for required environment variables
    if grep -q "OPENAI_API_KEY=" .env; then
        OPENAI_KEY=$(grep "OPENAI_API_KEY=" .env | cut -d'=' -f2)
        if [[ ${#OPENAI_KEY} -gt 10 ]]; then
            log_success "OpenAI API key configured"
            update_status "success"
        else
            log_error "OpenAI API key appears empty or invalid"
            update_status "error"
        fi
    else
        log_error "OPENAI_API_KEY not found in .env"
        update_status "error"
    fi
    
    if grep -q "PINECONE_API_KEY=" .env; then
        PINECONE_KEY=$(grep "PINECONE_API_KEY=" .env | cut -d'=' -f2)
        if [[ ${#PINECONE_KEY} -gt 10 ]]; then
            log_success "Pinecone API key configured"
            update_status "success"
        else
            log_error "Pinecone API key appears empty or invalid"
            update_status "error"
        fi
    else
        log_error "PINECONE_API_KEY not found in .env"
        update_status "error"
    fi
    
else
    log_error ".env file not found! Create it with your API keys"
    update_status "error"
fi
echo ""

# 7. Check Port Availability
log_section "Port Availability"

# Check port 8000 (Backend)
if ! lsof -i :8000 &> /dev/null; then
    log_success "Port 8000 available for backend"
    update_status "success"
else
    log_warning "Port 8000 is in use (may need to stop existing services)"
    update_status "warning"
fi

# Check port 3000 (Frontend)
if ! lsof -i :3000 &> /dev/null; then
    log_success "Port 3000 available for frontend"
    update_status "success"
else
    log_warning "Port 3000 is in use (may need to stop existing services)"
    update_status "warning"
fi
echo ""

# 8. Check Internet Connectivity
log_section "Internet Connectivity"

if ping -c 1 google.com &> /dev/null; then
    log_success "Internet connection available"
    update_status "success"
else
    log_warning "Internet connection check failed (needed for API calls)"
    update_status "warning"
fi

# Check API endpoints
if curl -s --head https://api.openai.com | head -n 1 | grep -q "200 OK"; then
    log_success "OpenAI API endpoint reachable"
    update_status "success"
else
    log_warning "Cannot reach OpenAI API (check network/firewall)"
    update_status "warning"
fi
echo ""

# Summary
echo -e "${BLUE}📊 Verification Summary${NC}"
echo -e "${BLUE}=====================${NC}"
echo -e "${GREEN}✅ Successes: $SUCCESSES${NC}"
echo -e "${YELLOW}⚠️  Warnings:  $WARNINGS${NC}"
echo -e "${RED}❌ Errors:    $ERRORS${NC}"
echo ""

# Final status
if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}🎉 All critical requirements met! You can proceed with installation.${NC}"
    echo -e "${CYAN}ℹ️  Run './start.sh' or '.\start.ps1' to start the application.${NC}"
    exit 0
elif [[ $ERRORS -le 2 && $WARNINGS -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  Minor issues detected but installation may work.${NC}"
    echo -e "${CYAN}ℹ️  Try running the startup script and check for errors.${NC}"
    exit 1
else
    echo -e "${RED}❌ Critical issues found! Please resolve errors before proceeding.${NC}"
    echo -e "${CYAN}ℹ️  Refer to SETUP_GUIDE.md for detailed installation instructions.${NC}"
    exit 2
fi