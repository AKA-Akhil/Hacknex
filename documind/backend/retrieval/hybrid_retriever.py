from backend.config import TOP_K, RRF_K, BM25_WEIGHT, DENSE_WEIGHT, CLIP_WEIGHT
from backend.indexing.vector_store import VectorStore
from backend.indexing.bm25_index import BM25Index
from backend.indexing.embeddings import TextEmbedder, ImageEmbedder
from backend.retrieval.query_classifier import classify
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

class RetrievedChunk:
    def __init__(self, chunk_id, text, content_type, doc_id, doc_name, page_number, score, image_path, metadata, retrieval_paths):
        self.chunk_id = chunk_id
        self.text = text
        self.content_type = content_type
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.page_number = page_number
        self.score = score
        self.image_path = image_path
        self.metadata = metadata
        self.retrieval_paths = retrieval_paths

def reciprocal_rank_fusion(ranked_lists: list[list[str]], weights: list[float], k: int = 60) -> list[tuple[str, float]]:
    scores = {}
    for ranked_list, weight in zip(ranked_lists, weights):
        for rank, chunk_id in enumerate(ranked_list):
            if chunk_id not in scores:
                scores[chunk_id] = 0.0
            scores[chunk_id] += weight * (1.0 / (k + rank + 1))
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def retrieve(query: str, top_k=TOP_K, doc_filter: list[str] = None) -> list[RetrievedChunk]:
    classification = classify(query)
    
    v_store = VectorStore()
    bm25 = BM25Index()
    text_embedder = TextEmbedder()
    image_embedder = ImageEmbedder()
    
    # Paths
    bm25_ranked = []
    dense_ranked = []
    clip_ranked = []
    
    # Path A: BM25
    bm25_res = bm25.query(query, top_k * 2)
    # doc filter
    if doc_filter:
        filtered_bm25 = []
        for cid, score in bm25_res:
            meta = bm25.get_chunk_by_id(cid)
            if meta and meta.get("doc_id") in doc_filter:
                filtered_bm25.append(cid)
        bm25_ranked = filtered_bm25
    else:
        bm25_ranked = [cid for cid, score in bm25_res]
        
    # Path B: Dense
    query_emb = text_embedder.embed_query(query)
    filter_dict = {"doc_id": {"$in": doc_filter}} if doc_filter else None
    
    dense_res = v_store.query_text(query_emb, top_k * 2, filter_dict=filter_dict)
    dense_ranked = [res["chunk_id"] for res in dense_res]
    
    # Path C: CLIP (Visual)
    if classification["needs_visual"]:
        clip_emb = image_embedder.embed_text(query)
        clip_res = v_store.query_visual(clip_emb, top_k * 2, filter_dict=filter_dict)
        clip_ranked = [res["chunk_id"] for res in clip_res]
        
    # RRF
    lists = [bm25_ranked, dense_ranked, clip_ranked]
    weights = [BM25_WEIGHT, DENSE_WEIGHT, CLIP_WEIGHT]
    
    rrf_scores = reciprocal_rank_fusion(lists, weights, k=RRF_K)
    
    # Map back to objects
    results = []
    for chunk_id, score in rrf_scores[:top_k * 2]: # get a bit more for boosting
        meta = bm25.get_chunk_by_id(chunk_id)
        if not meta:
            continue
            
        c_type = meta.get("content_type", "text")
        
        # Content type boosting
        final_score = score
        if classification["needs_table"] and c_type == "table":
            final_score *= 1.2
        if classification["needs_visual"] and c_type == "chart":
            final_score *= 1.2
            
        # Determine paths
        paths = []
        if chunk_id in bm25_ranked: paths.append("bm25")
        if chunk_id in dense_ranked: paths.append("dense")
        if chunk_id in clip_ranked: paths.append("clip")
            
        results.append(RetrievedChunk(
            chunk_id=chunk_id,
            text=meta.get("text", ""),
            content_type=c_type,
            doc_id=meta.get("doc_id", ""),
            doc_name=meta.get("doc_name", ""),
            page_number=int(meta.get("page_number", 1)),
            score=final_score,
            image_path=meta.get("image_path"),
            metadata=meta,
            retrieval_paths=paths
        ))
        
    # Re-sort after boosting
    results = sorted(results, key=lambda x: x.score, reverse=True)[:top_k]
    return results
