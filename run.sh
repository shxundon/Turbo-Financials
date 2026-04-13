#!/bin/bash

# Turbo Financials Form Handler - Startup Script for macOS/Linux

echo ""
echo "========================================="
echo "   Turbo Financials Form Handler"
echo "   Starting Flask Application"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Clear any existing logs
if [ -d "logs" ]; then
    echo "Clearing old logs..."
    rm -f logs/*.log
fi

# Run the Flask application
echo ""
echo "========================================="
echo "   Application Starting..."
echo "========================================="
echo ""
echo "Home Page:      http://localhost:5000/"
echo "Admin Panel:    http://localhost:5000/admin/summary"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python app.py
