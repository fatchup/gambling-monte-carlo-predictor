#!/bin/bash

# Windows Build Script for Parlay Simulator
# Usage: bash build_windows.sh (or run from PowerShell)

echo "🎲 Building Parlay Simulator for Windows..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install pyinstaller

# Build the app
echo "Building Parlay Simulator.exe..."
pyinstaller "Parlay Simulator.spec"

# Verify build
if [ -f "dist/Parlay Simulator.exe" ]; then
    echo "✅ Build successful!"
    echo "📦 EXE location: dist/Parlay Simulator.exe"
else
    echo "❌ Build failed!"
    exit 1
fi

deactivate
