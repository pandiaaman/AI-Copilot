#!/bin/bash
# Stop script for MediaCentral CTMS Chatbot (Unix/macOS)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}🛑 Stopping MediaCentral CTMS Chatbot Services...${NC}"

# Function to kill process by PID file
kill_by_pidfile() {
    local pidfile=$1
    local name=$2
    
    if [ -f "$pidfile" ]; then
        local pid=$(cat "$pidfile")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            echo -e "${GREEN}✅ Stopped $name (PID: $pid)${NC}"
        else
            echo -e "${YELLOW}⚠️  $name process not running${NC}"
        fi
        rm -f "$pidfile"
    fi
}

# Stop by PID files
kill_by_pidfile "logs/backend.pid" "FastAPI backend"
kill_by_pidfile "logs/frontend.pid" "React frontend"

# Kill any remaining processes on ports
echo -e "${YELLOW}Checking for remaining processes on ports 8000 and 3000...${NC}"

# Kill process on port 8000
PID_8000=$(lsof -ti:8000 2>/dev/null || true)
if [ ! -z "$PID_8000" ]; then
    kill -9 $PID_8000
    echo -e "${GREEN}✅ Killed remaining process on port 8000${NC}"
fi

# Kill process on port 3000
PID_3000=$(lsof -ti:3000 2>/dev/null || true)
if [ ! -z "$PID_3000" ]; then
    kill -9 $PID_3000
    echo -e "${GREEN}✅ Killed remaining process on port 3000${NC}"
fi

echo -e "${GREEN}🎉 All services stopped successfully!${NC}"