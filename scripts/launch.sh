#!/bin/bash

# ANISA Easy Launcher Script
# Makes it super easy to launch ANISA demos from anywhere!

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go to the project root (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🌍============================================================🌍"
echo "🚀 ANISA - Easy Launcher 🚀"
echo "🌍============================================================🌍"
echo

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected!"
    echo "   Activating virtual environment..."
    source "$PROJECT_ROOT/anisa-venv/bin/activate"
    echo "✅ Virtual environment activated!"
    echo
fi

echo "🎯 Choose your demo:"
echo "1) 🎭 Interactive Demo (Recommended)"
echo "2) 🌐 Web Demo (Open in browser)"
echo "3) 🚀 API Server (Start web service)"
echo "4) 💻 CLI Demo (Command line)"
echo "5) 📊 Quick Demo (Fast showcase)"
echo "6) 🚀 GTCX Integration Demo (Business focused)"
echo "7) 🚪 Exit"
echo

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo "🎭 Launching Interactive Demo..."
        python "$PROJECT_ROOT/demos/interactive_demo.py"
        ;;
    2)
        echo "🌐 Opening Web Demo..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open "$PROJECT_ROOT/web_demo/index.html"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            xdg-open "$PROJECT_ROOT/web_demo/index.html"
        else
            start "$PROJECT_ROOT/web_demo/index.html"
        fi
        echo "✅ Web demo opened in your browser!"
        ;;
    3)
        echo "🚀 Starting API Server..."
        echo "This will start the ANISA web API on http://localhost:8000"
        echo "Press Ctrl+C to stop the server"
        python "$PROJECT_ROOT/scripts/start_api.py"
        ;;
    4)
        echo "💻 Launching CLI Demo..."
        python "$PROJECT_ROOT/src/cli.py" --demo
        ;;
    5)
        echo "📊 Running Quick Demo..."
        python "$PROJECT_ROOT/demos/demo.py"
        ;;
    6)
        echo "🚀 Running GTCX Integration Demo..."
        python "$PROJECT_ROOT/demos/gtcx_demo.py"
        ;;
    7)
        echo "👋 Thank you for using ANISA!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
