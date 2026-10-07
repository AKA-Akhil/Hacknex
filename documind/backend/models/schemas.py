from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum

class ContentType(str, Enum):
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    IMAGE = "image"

class DocumentStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"

class UploadResponse(BaseModel):
    doc_id: str
    doc_name: str
    status: DocumentStatus
    total_pages: int
    total_chunks: int
    content_summary: dict  # {"text_chunks": N, "table_chunks": N, "visual_chunks": N}
    message: str

class QueryRequest(BaseModel):
    question: str
    doc_ids: Optional[list[str]] = None  # None = search all docs

class Citation(BaseModel):
    source_number: int
    doc_id: str
    doc_name: str
    page_number: int
    content_type: ContentType
    chunk_text: str
    image_path: Optional[str] = None
    score: float
    retrieval_paths: list[str]

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    query_classification: dict
    retrieval_stats: dict  # {"total_chunks_searched": N, "retrieval_time_ms": N}

class DocumentInfo(BaseModel):
    doc_id: str
    doc_name: str
    status: DocumentStatus
    total_pages: int
    total_chunks: int
    upload_time: str
    content_summary: dict

class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    models_available: list[str]
    total_documents: int
    total_chunks: int
