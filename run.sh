#!/bin/bash

# Venv setup
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Install playwright
echo "Installing playwright chromium..."
playwright install chromium

# Run app
echo "Launching Product Image Matcher Pro..."
python app.py
