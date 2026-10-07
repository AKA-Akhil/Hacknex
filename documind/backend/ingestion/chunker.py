from backend.config import CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_SIZE
from backend.utils.helpers import setup_logger, generate_id
from backend.ingestion.pdf_parser import ContentBlock

logger = setup_logger(__name__)

class Chunk:
    def __init__(self, chunk_id, doc_id, doc_name, page_number, content_type, text, image_path=None, metadata=None):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.page_number = page_number
        self.content_type = content_type
        self.text = text
        self.image_path = image_path
        self.metadata = metadata or {}

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list[str]:
    """Splits text into chunks with sliding window overlap based on word approximation (tokens)."""
    words = text.split()
    if not words:
        return []
        
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.split()) >= MIN_CHUNK_SIZE or i == 0:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def chunk_blocks(blocks: list[ContentBlock]) -> list[Chunk]:
    """Converts ContentBlocks into indexable Chunks."""
    chunks = []
    
    for block in blocks:
        base_metadata = {
            "block_id": block.block_id,
            "bbox": str(block.bbox) if block.bbox else "",
            **block.metadata
        }
        
        if block.content_type == "text":
            text_chunks = chunk_text(block.content)
            for i, tc in enumerate(text_chunks):
                chunks.append(Chunk(
                    chunk_id=generate_id(),
                    doc_id=block.doc_id,
                    doc_name=block.doc_name,
                    page_number=block.page_number,
                    content_type="text",
                    text=tc,
                    metadata={"chunk_index": i, **base_metadata}
                ))
        
        elif block.content_type == "table":
            # Don't split tables unless strictly necessary, but simple approach keeps as 1
            chunks.append(Chunk(
                chunk_id=generate_id(),
                doc_id=block.doc_id,
                doc_name=block.doc_name,
                page_number=block.page_number,
                content_type="table",
                text=block.content,
                metadata=base_metadata
            ))
            
        elif block.content_type == "chart":
            chunks.append(Chunk(
                chunk_id=generate_id(),
                doc_id=block.doc_id,
                doc_name=block.doc_name,
                page_number=block.page_number,
                content_type="chart",
                text=block.content,
                image_path=block.image_path,
                metadata=base_metadata
            ))
            
    return chunks
