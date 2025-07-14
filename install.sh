#!/bin/bash

echo "🔄 Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "📦 Installing Python and required tools..."
pkg install -y python git curl

echo "📄 Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Installation complete. You can now run: bash run_all.sh"