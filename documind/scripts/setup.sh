#!/bin/bash
cd "$(dirname "$0")/.."
echo "=== DocuMind Setup ==="

# Check Python
python3 --version || { echo "Python 3.11+ required"; exit 1; }

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create storage dirs
mkdir -p storage/{uploads,page_images,chart_crops,chroma_db}

# Check Tesseract
tesseract --version || echo "WARNING: Install Tesseract OCR"

# Check Ollama
ollama --version || echo "WARNING: Install Ollama from https://ollama.com"

# Pull models
echo "Pulling Ollama models (this takes a while)..."
ollama pull moondream
ollama pull mistral:7b-instruct-q4_K_M

# Frontend setup
cd ../frontend
npm install

echo "=== Setup Complete ==="
echo "Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "Start frontend: cd frontend && npm run dev"
