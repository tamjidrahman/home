#!/bin/bash
poetry install

# Copy main.py to ~/.local/bin/homeassistant-cli
cp $(poetry run which home) ~/.local/bin/home

# Make the script executable
chmod +x ~/.local/bin/home

echo "Installation complete. The 'home' app is now available in ~/.local/bin"
