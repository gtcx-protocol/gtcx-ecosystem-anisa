#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

cd "${PROJECT_ROOT}"

echo "🚀 Setting up ANISA training environment"

if [ -d "anisa-venv" ]; then
  source anisa-venv/bin/activate
else
  python3 -m venv anisa-venv
  source anisa-venv/bin/activate
fi

python -m pip install --upgrade pip
pip install -r requirements-training.txt

echo "🧠 Running quick-start training..."
python scripts/quick_start_training.py

echo "✅ Training complete"



