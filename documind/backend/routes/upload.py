from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from backend.models.schemas import UploadResponse, DocumentStatus
from backend.config import UPLOAD_DIR
from backend.utils.helpers import generate_id, setup_logger
from backend.ingestion.pdf_parser import parse_pdf
from backend.ingestion.chunker import chunk_blocks
from backend.indexing.embeddings import TextEmbedder, ImageEmbedder
from backend.indexing.vector_store import VectorStore
from backend.indexing.bm25_index import BM25Index
import shutil
import os
import time

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/upload", tags=["upload"])

# Global state for document status (in a real app, use a DB)
document_statuses = {}
document_summaries = {}
document_names = {}

def process_document_task(doc_id: str, file_path: str, doc_name: str):
    try:
        document_statuses[doc_id] = DocumentStatus.PROCESSING
        
        # 1. Parse PDF
        logger.info(f"Parsing {doc_name}...")
        blocks = parse_pdf(file_path, doc_id, doc_name)
        
        if not blocks:
            document_statuses[doc_id] = DocumentStatus.ERROR
            logger.error(f"Failed to extract any content from {doc_name}")
            return
            
        # 2. Chunk
        logger.info(f"Chunking {doc_name}...")
        chunks = chunk_blocks(blocks)
        
        # Calculate summary
        text_chunks = sum(1 for c in chunks if c.content_type == "text")
        table_chunks = sum(1 for c in chunks if c.content_type == "table")
        visual_chunks = sum(1 for c in chunks if c.content_type == "chart")
        
        document_summaries[doc_id] = {
            "total_pages": max([c.page_number for c in chunks]) if chunks else 0,
            "total_chunks": len(chunks),
            "content_summary": {
                "text_chunks": text_chunks,
                "table_chunks": table_chunks,
                "visual_chunks": visual_chunks
            },
            "upload_time": str(time.time()),
            "doc_name": doc_name
        }
        
        # 3. Embed
        logger.info(f"Embedding {doc_name}...")
        text_embedder = TextEmbedder()
        image_embedder = ImageEmbedder()
        
        text_embeddings = text_embedder.embed([c.text for c in chunks])
        
        image_embeddings = []
        for c in chunks:
            if c.content_type == "chart" and c.image_path:
                image_embeddings.append(image_embedder.embed_image(c.image_path))
            else:
                image_embeddings.append(None)
                
        # 4. Store
        logger.info(f"Storing {doc_name}...")
        v_store = VectorStore()
        v_store.add_chunks(chunks, text_embeddings, image_embeddings)
        
        bm25 = BM25Index()
        bm25.add_chunks(chunks)
        
        document_statuses[doc_id] = DocumentStatus.READY
        logger.info(f"Finished processing {doc_name}")
        
    except Exception as e:
        logger.error(f"Error processing {doc_name}: {e}", exc_info=True)
        document_statuses[doc_id] = DocumentStatus.ERROR

@router.post("", response_model=UploadResponse)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    doc_id = generate_id()
    file_path = str(UPLOAD_DIR / f"{doc_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    document_statuses[doc_id] = DocumentStatus.UPLOADING
    document_names[doc_id] = file.filename
    
    background_tasks.add_task(process_document_task, doc_id, file_path, file.filename)
    
    return UploadResponse(
        doc_id=doc_id,
        doc_name=file.filename,
        status=DocumentStatus.UPLOADING,
        total_pages=0,
        total_chunks=0,
        content_summary={},
        message="Upload started. Processing in background."
    )

@router.get("/status/{doc_id}")
async def get_status(doc_id: str):
    status = document_statuses.get(doc_id, "unknown")
    summary = document_summaries.get(doc_id, {})
    return {"doc_id": doc_id, "status": status, **summary}
