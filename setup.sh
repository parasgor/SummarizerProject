#!/bin/bash

# Summarizer Agent - Quick Start Setup Script
# This script sets up the development environment

set -e

echo "🚀 Summarizer Agent - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "1️⃣  Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"
echo ""

# Create virtual environment
echo "2️⃣  Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "3️⃣  Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "4️⃣  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "5️⃣  Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Setup environment file
echo "6️⃣  Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo "⚠️  Please update .env with your OpenAI API key"
else
    echo "✓ .env file already exists"
fi
echo ""

# Run tests
echo "7️⃣  Running tests..."
if pytest tests/ -q > /dev/null 2>&1; then
    echo "✓ All tests passed!"
else
    echo "⚠️  Some tests failed. Run 'pytest -v' for details"
fi
echo ""

echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your OpenAI API key"
echo "2. Run examples: python examples/basic_usage.py"
echo "3. Run tests: pytest tests/ -v"
echo "4. Read the README for more information"
echo ""
echo "Happy summarizing! 🎉"
