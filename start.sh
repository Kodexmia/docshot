#!/bin/bash
# Quick start script for Overlay Annotator

echo "=================================================="
echo "Overlay Annotator v2 - Quick Start"
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run tests
echo ""
echo "Running quick tests..."
python test_quick.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "🚀 Starting Overlay Annotator..."
    echo "=================================================="
    echo ""
    echo "Press Ctrl+Alt+S to capture screen region"
    echo ""
    python -m app.main
else
    echo ""
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi
