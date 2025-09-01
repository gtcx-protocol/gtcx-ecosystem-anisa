#!/bin/bash
# ANISA Web Demo Launcher
# Open the web demo in your browser from anywhere!

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go to the project root (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🌐 Opening ANISA Web Demo... 🌐"

# Check if the web demo file exists
if [[ ! -f "$PROJECT_ROOT/web_demo/index.html" ]]; then
    echo "❌ Web demo not found at: $PROJECT_ROOT/web_demo/index.html"
    exit 1
fi

# Open web demo based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$PROJECT_ROOT/web_demo/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$PROJECT_ROOT/web_demo/index.html"
else
    # Windows
    start "$PROJECT_ROOT/web_demo/index.html"
fi

echo "✅ Web demo opened in your browser!"
echo "🌐 If it didn't open automatically, navigate to: $PROJECT_ROOT/web_demo/index.html"
