from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.models.schemas import DocumentInfo
from backend.routes.upload import document_statuses, document_summaries
from backend.indexing.vector_store import VectorStore
from backend.indexing.bm25_index import BM25Index
from backend.config import PAGE_IMAGES_DIR, CHART_CROPS_DIR
import os
import glob

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.get("", response_model=list[DocumentInfo])
async def list_documents():
    docs = []
    for doc_id, status in document_statuses.items():
        summary = document_summaries.get(doc_id, {})
        docs.append(DocumentInfo(
            doc_id=doc_id,
            doc_name=summary.get("doc_name", f"Document {doc_id[:8]}"),
            status=status,
            total_pages=summary.get("total_pages", 0),
            total_chunks=summary.get("total_chunks", 0),
            upload_time=summary.get("upload_time", ""),
            content_summary=summary.get("content_summary", {})
        ))
    return docs

@router.get("/{doc_id}", response_model=DocumentInfo)
async def get_document(doc_id: str):
    status = document_statuses.get(doc_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Document not found")
    summary = document_summaries.get(doc_id, {})
    return DocumentInfo(
        doc_id=doc_id,
        doc_name=summary.get("doc_name", f"Document {doc_id[:8]}"),
        status=status,
        total_pages=summary.get("total_pages", 0),
        total_chunks=summary.get("total_chunks", 0),
        upload_time=summary.get("upload_time", ""),
        content_summary=summary.get("content_summary", {})
    )

@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    if doc_id in document_statuses:
        del document_statuses[doc_id]
    if doc_id in document_summaries:
        del document_summaries[doc_id]
        
    VectorStore().delete_document(doc_id)
    BM25Index().delete_document(doc_id)
    
    return {"status": "deleted"}

@router.get("/{doc_id}/page/{page_num}/image")
async def get_page_image(doc_id: str, page_num: int):
    # E.g. {doc_id}_page_{page_num}.png
    pattern = str(PAGE_IMAGES_DIR / f"{doc_id}_page_{page_num}.png")
    matches = glob.glob(pattern)
    if not matches:
        raise HTTPException(status_code=404, detail="Page image not found")
    return FileResponse(matches[0])
