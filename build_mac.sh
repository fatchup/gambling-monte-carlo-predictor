#!/bin/bash

# macOS Build Script for Parlay Simulator
# Usage: bash build_mac.sh

echo "🎲 Building Parlay Simulator for macOS..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install tkinter pyinstaller

# Build the app
echo "Building Parlay Simulator.app..."
pyinstaller "Parlay Simulator.spec"

# Verify build
if [ -d "dist/Parlay Simulator.app" ]; then
    echo "✅ Build successful!"
    echo "📦 App location: dist/Parlay Simulator.app"
    echo ""
    echo "To run the app:"
    echo "  open dist/Parlay\ Simulator.app"
else
    echo "❌ Build failed!"
    exit 1
fi

deactivate
