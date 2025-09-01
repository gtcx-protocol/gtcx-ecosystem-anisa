#!/bin/bash
# ANISA Quick Demo
# Run the quick demo from anywhere!

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Go to the project root (one level up from scripts)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🌍 ANISA Quick Demo Starting... 🌍"
echo "=================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected!"
    echo "   Activating virtual environment..."
    source "$PROJECT_ROOT/anisa-venv/bin/activate"
    echo "✅ Virtual environment activated!"
    echo
fi

# Run the quick demo
python "$PROJECT_ROOT/demos/demo.py"
