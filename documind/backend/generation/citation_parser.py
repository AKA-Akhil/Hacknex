import re
from backend.models.schemas import Citation, ContentType
from backend.retrieval.hybrid_retriever import RetrievedChunk

def parse_citations(llm_output: str, source_mapping: dict[int, RetrievedChunk]) -> dict:
    """Parses [Source N] citations and maps them back to metadata."""
    # Find all unique source numbers mentioned
    # Matches [Source 1], [Source 1, Source 2], [Source 1, 2], etc.
    citations = []
    mentioned_sources = set()
    
    # Simple regex to find numbers inside [Source ...]
    matches = re.finditer(r'\[Source(s)?\s+([0-9\s,]+)\]', llm_output)
    
    for match in matches:
        nums_str = match.group(2)
        # Extract digits
        nums = [int(n) for n in re.findall(r'\d+', nums_str)]
        mentioned_sources.update(nums)
        
    for num in mentioned_sources:
        if num in source_mapping:
            chunk = source_mapping[num]
            citations.append(Citation(
                source_number=num,
                doc_id=chunk.doc_id,
                doc_name=chunk.doc_name,
                page_number=chunk.page_number,
                content_type=ContentType(chunk.content_type),
                chunk_text=chunk.text,
                image_path=chunk.image_path,
                score=chunk.score,
                retrieval_paths=chunk.retrieval_paths
            ))
            
    # Sort by source number
    citations = sorted(citations, key=lambda c: c.source_number)
    
    return {
        "answer": llm_output,
        "citations": citations
    }
    
def validate_citations(citations: list[Citation], answer: str) -> list[dict]:
    # Placeholder for more complex validation if needed
    # The parsing logic already ignores hallucinated numbers because it checks source_mapping
    return citations
