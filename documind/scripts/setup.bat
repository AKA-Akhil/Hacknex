@echo off
cd /d "%~dp0.."
echo === DocuMind Setup ===

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.11+ required
    exit /b 1
)

REM Backend setup
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

REM Create storage dirs
mkdir storage\uploads 2>nul
mkdir storage\page_images 2>nul
mkdir storage\chart_crops 2>nul
mkdir storage\chroma_db 2>nul

REM Check Tesseract
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Install Tesseract OCR
)

REM Check Ollama
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Install Ollama from https://ollama.com
)

REM Pull models
echo Pulling Ollama models (this takes a while)...
ollama pull moondream
ollama pull mistral:7b-instruct-q4_K_M

REM Frontend setup
cd ..\frontend
call npm install

echo === Setup Complete ===
echo Start backend: cd backend ^&^& call venv\Scripts\activate ^&^& uvicorn main:app --reload
echo Start frontend: cd frontend ^&^& npm run dev
