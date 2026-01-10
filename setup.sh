#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete! Don't forget to:"
echo "1. Create a .env file with your API keys (see env_template.txt for reference)"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the research assistant: python main.py"
