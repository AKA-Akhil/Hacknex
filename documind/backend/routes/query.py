from fastapi import APIRouter
import time
from backend.models.schemas import QueryRequest, QueryResponse
from backend.retrieval.hybrid_retriever import retrieve
from backend.retrieval.query_classifier import classify
from backend.generation.prompt_builder import build_prompt
from backend.generation.llm_generator import generate
from backend.generation.citation_parser import parse_citations

router = APIRouter(prefix="/api/query", tags=["query"])

@router.post("", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    start_time = time.time()
    
    # 1. Classify
    classification = classify(request.question)
    
    # 2. Retrieve
    retrieved_chunks = retrieve(request.question, doc_filter=request.doc_ids)
    
    # 3. Build Prompt
    prompt, source_mapping = build_prompt(request.question, retrieved_chunks)
    
    # 4. Generate
    answer_text = generate(prompt)
    
    # 5. Parse Citations
    result = parse_citations(answer_text, source_mapping)
    
    retrieval_time = int((time.time() - start_time) * 1000)
    
    return QueryResponse(
        answer=result["answer"],
        citations=result["citations"],
        query_classification=classification,
        retrieval_stats={
            "total_chunks_searched": len(retrieved_chunks), # simplified
            "retrieval_time_ms": retrieval_time
        }
    )
