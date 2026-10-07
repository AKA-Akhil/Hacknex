import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import PAGE_IMAGES_DIR, CHART_CROPS_DIR
from backend.routes import upload, query, documents, health
from backend.indexing.embeddings import TextEmbedder, ImageEmbedder
from backend.indexing.vector_store import VectorStore
from backend.indexing.bm25_index import BM25Index
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DocuMind API — initializing singletons...")
    TextEmbedder()
    ImageEmbedder()
    VectorStore()
    BM25Index()
    logger.info("All singletons initialized.")
    yield

app = FastAPI(title="DocuMind API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(query.router)
app.include_router(documents.router)
app.include_router(health.router)

app.mount("/static/pages", StaticFiles(directory=str(PAGE_IMAGES_DIR)), name="page_images")
app.mount("/static/charts", StaticFiles(directory=str(CHART_CROPS_DIR)), name="chart_crops")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
