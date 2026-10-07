from backend.config import SYSTEM_PROMPT
from backend.retrieval.hybrid_retriever import RetrievedChunk

def build_prompt(query: str, retrieved_chunks: list[RetrievedChunk]) -> tuple[str, dict]:
    """Builds the LLM prompt and returns (prompt, source_mapping)."""
    source_mapping = {}
    
    evidence_blocks = []
    
    for i, chunk in enumerate(retrieved_chunks, start=1):
        source_mapping[i] = chunk
        
        block = f"[Source {i}] (Document: {chunk.doc_name} | Page: {chunk.page_number} | Type: {chunk.content_type})\n"
        
        if chunk.content_type == "chart":
            block += f"Description: {chunk.text}\n"
        else:
            block += f"{chunk.text}\n"
            
        evidence_blocks.append(block)
        
    evidence_str = "\n".join(evidence_blocks)
    
    # Simple truncation to avoid blowing up context window (very naive approximation)
    max_evidence_chars = 4000 * 4 # ~4000 tokens
    if len(evidence_str) > max_evidence_chars:
        evidence_str = evidence_str[:max_evidence_chars] + "\n... (evidence truncated)"
        
    prompt = f"Evidence:\n\n{evidence_str}\n\n---\n\nQuestion: {query}\n\nAnswer the question using ONLY the evidence above. Cite every claim using [Source N] format."
    
    return prompt, source_mapping
