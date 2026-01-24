#!/bin/bash

# macOS Build & ZIP Script for Parlay Simulator
# Creates a distributable ZIP file for Mac users
# Usage: bash build_and_zip_mac.sh

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
pip install pyinstaller

# Build the app
echo "Building Parlay Simulator.app..."
pyinstaller "Parlay Simulator.spec"

# Verify build
if [ -d "dist/Parlay Simulator.app" ]; then
    echo "✅ Build successful!"
    
    # Create ZIP file
    echo "📦 Creating ZIP file..."
    cd dist
    zip -r "Parlay Simulator.zip" "Parlay Simulator.app" -q
    cd ..
    
    if [ -f "dist/Parlay Simulator.zip" ]; then
        FILE_SIZE=$(du -h "dist/Parlay Simulator.zip" | cut -f1)
        echo "✅ ZIP created successfully!"
        echo ""
        echo "📥 Download ready: dist/Parlay Simulator.zip"
        echo "📊 File size: $FILE_SIZE"
        echo ""
        echo "Share this file with Mac users. They can:"
        echo "  1. Download and unzip the file"
        echo "  2. Double-click 'Parlay Simulator.app' to run"
    else
        echo "❌ ZIP creation failed!"
        exit 1
    fi
else
    echo "❌ Build failed!"
    exit 1
fi

deactivate
