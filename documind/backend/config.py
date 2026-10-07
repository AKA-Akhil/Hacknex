import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
PAGE_IMAGES_DIR = STORAGE_DIR / "page_images"
CHART_CROPS_DIR = STORAGE_DIR / "chart_crops"
CHROMA_DB_DIR = STORAGE_DIR / "chroma_db"

# Create dirs on import
for d in [UPLOAD_DIR, PAGE_IMAGES_DIR, CHART_CROPS_DIR, CHROMA_DB_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
VISION_MODEL = "moondream"
LLM_MODEL = "mistral:7b-instruct-q4_K_M"

# Embedding
TEXT_EMBED_MODEL = "all-MiniLM-L6-v2"
CLIP_MODEL_NAME = "ViT-B-32"
CLIP_PRETRAINED = "laion2b_s34b_b79k"

# Chunking
CHUNK_SIZE = 400          # tokens
CHUNK_OVERLAP = 50        # tokens
MIN_CHUNK_SIZE = 50       # skip tiny chunks

# Retrieval
TOP_K = 10                # chunks to retrieve
RRF_K = 60                # RRF constant
BM25_WEIGHT = 1.0
DENSE_WEIGHT = 1.0
CLIP_WEIGHT = 0.8

# ChromaDB collection names
TEXT_COLLECTION = "text_chunks"
VISUAL_COLLECTION = "visual_chunks"

# Table detection
MIN_TABLE_ROWS = 2
MIN_TABLE_COLS = 2

# OCR
OCR_CONFIDENCE_THRESHOLD = 30  # below this, page is likely scanned
TESSERACT_CONFIG = "--oem 3 --psm 6"

# Vision description
VISION_PROMPT = """Analyze this image from a document. Describe in detail:
1. What type of visual is this? (bar chart, line graph, pie chart, diagram, flowchart, photo, etc.)
2. What data or information does it show?
3. What are the axis labels, legends, and values if applicable?
4. What are the key trends, comparisons, or takeaways?
Be precise with numbers and labels you can see."""

# Answer generation
SYSTEM_PROMPT = """You are DocuMind, a document analysis assistant. You answer questions ONLY using the provided evidence chunks. Every claim MUST cite its source using [Source N] format.

Rules:
1. ONLY use information from the provided evidence. Never make up data.
2. EVERY factual claim must have a citation like [Source 1] or [Source 2, Source 3].
3. If evidence is insufficient, say so explicitly.
4. For numerical questions, show exact numbers from the evidence.
5. When comparing data from tables and charts, note if values align or conflict.
6. Reference the content type (text/table/chart) when it adds clarity.

Format your answer as:
- Clear, structured prose with inline citations
- End with a "Sources Used" summary listing each source's document, page, and type"""
