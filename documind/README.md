# DocuMind — Multimodal Document Intelligence System

A fully local web application where users upload PDF documents (containing text, tables, charts, graphs, and scanned pages) and ask natural language questions. The system finds answers by analyzing ALL content types natively, combines evidence from multiple modalities, and returns cited answers pointing to exact pages, content types, and regions.

## 🌟 Features
- **Triple-path hybrid retrieval:** Combines BM25 sparse retrieval, dense semantic search (SentenceTransformers), and visual search (CLIP) merged seamlessly with Reciprocal Rank Fusion (RRF).
- **Vision-Language Analysis:** Uses `moondream` (via Ollama) to interpret and describe charts, graphs, and images during ingestion.
- **Accurate Citations:** Answers are generated using `mistral:7b` with strict formatting to trace every claim back to the exact chunk and page.
- **Privacy-First & Local:** 100% local processing. No paid APIs, no subscriptions. All vectors are stored locally in ChromaDB and BM25 persistent indexes.

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS, Framer Motion
- **Backend:** FastAPI, Python, Uvicorn
- **AI/ML:** Ollama (Mistral, Moondream), SentenceTransformers, CLIP, ChromaDB, Rank-BM25
- **Document Processing:** PyMuPDF, pdfplumber, Tesseract OCR, Poppler

## ⚠️ Prerequisites

You MUST install the following system dependencies before running:

1. **Python 3.10 or 3.11** 
   - *Important:* Python 3.12+ (including 3.14) is currently incompatible with several ML libraries unless you manually compile from source. Please stick to 3.10 or 3.11!
2. **Ollama**: Download from [ollama.com](https://ollama.com/)
3. **Tesseract OCR**: 
   - Windows: [Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Ensure it's added to your system PATH).
4. **Poppler**:
   - Windows: Download [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add the `bin/` folder to your system PATH.

## 🚀 Setup

1. Run the setup script to create your virtual environment, install Python dependencies, pull Ollama models, and install Node.js modules:
   - **Windows:** Run `scripts\setup.bat`
   - **Linux/Mac:** Run `bash scripts/setup.sh`

*(Note: The setup script will pull the `moondream` and `mistral` models via Ollama. This is several gigabytes of data and may take some time depending on your internet connection.)*

## 💻 Running the Application

### 1. Start the Backend
Open a terminal in the `documind` folder:
```bash
cd backend
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
uvicorn main:app --reload
```
The backend will run on `http://localhost:8000`.

### 2. Start the Frontend
Open a new terminal in the `documind` folder:
```bash
cd frontend
npm run dev
```
The frontend will run on `http://localhost:5173`. Open this URL in your browser.

## 📄 Testing
Please refer to `sample_docs/README.md` for instructions on how to create the ideal test documents for this system to demonstrate its multimodal capabilities!
