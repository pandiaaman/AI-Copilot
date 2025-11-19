#!/bin/bash

# CTMS Chatbot Environment Activation Script
# Run this script with: source activate_env.sh

echo "🚀 Activating CTMS Chatbot virtual environment..."

# Activate the virtual environment
source venv/bin/activate

# Check if activation was successful
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activated successfully!"
    echo "📍 Environment: $VIRTUAL_ENV"
    echo "🐍 Python version: $(python --version)"
    echo ""
    echo "🎯 You can now run:"
    echo "   - cd alltypes && python ingestion-alltypes-improved.py"
    echo "   - cd 'fastapi app' && uvicorn app-improved:app --reload"
    echo ""
    echo "💡 To deactivate later, just run: deactivate"
else
    echo "❌ Failed to activate virtual environment"
    echo "Make sure you run this script from the AvidChatbot directory"
fi