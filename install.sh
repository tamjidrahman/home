#!/bin/bash
poetry install

# Copy main.py to ~/.local/bin/homeassistant-cli
cp $(poetry run which home) ~/.local/bin/home
echo "Created ~/.local/bin/home"

mkdir -p ~/.config/home
cp config.toml ~/.config/home/config.toml
echo "Created ~/.config/home/config.toml"

# Make the script executable
chmod +x ~/.local/bin/home

echo "Installation complete. The 'home' app is now available in ~/.local/bin. Config loaded to ~/.config/home/config.toml"
