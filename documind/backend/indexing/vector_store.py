import chromadb
from backend.config import CHROMA_DB_DIR, TEXT_COLLECTION, VISUAL_COLLECTION
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

class VectorStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStore, cls).__new__(cls)
            logger.info("Initializing ChromaDB client...")
            cls._instance.client = chromadb.PersistentClient(
                path=str(CHROMA_DB_DIR)
            )
            
            # Create collections
            cls._instance.text_collection = cls._instance.client.get_or_create_collection(
                name=TEXT_COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
            
            cls._instance.visual_collection = cls._instance.client.get_or_create_collection(
                name=VISUAL_COLLECTION,
                metadata={"hnsw:space": "cosine"}
            )
        return cls._instance

    def add_chunks(self, chunks: list, text_embeddings: list[list[float]], image_embeddings: list[list[float]] = None):
        """Adds chunks to ChromaDB."""
        if not chunks:
            return
            
        text_ids = []
        text_docs = []
        text_metadatas = []
        text_embeds = []
        
        vis_ids = []
        vis_metadatas = []
        vis_embeds = []
        
        for i, chunk in enumerate(chunks):
            # For Text Collection
            text_ids.append(chunk.chunk_id)
            text_docs.append(chunk.text)
            
            meta = {
                "doc_id": chunk.doc_id,
                "doc_name": chunk.doc_name,
                "page_number": chunk.page_number,
                "content_type": chunk.content_type,
                "image_path": chunk.image_path if chunk.image_path else ""
            }
            # Chroma metadata values must be str, int, float, bool
            safe_meta = {k: str(v) if v is not None else "" for k, v in meta.items()}
            text_metadatas.append(safe_meta)
            text_embeds.append(text_embeddings[i])
            
            # For Visual Collection
            if chunk.content_type == "chart" and chunk.image_path and image_embeddings and image_embeddings[i]:
                vis_ids.append(chunk.chunk_id)
                vis_metadatas.append(safe_meta)
                vis_embeds.append(image_embeddings[i])
                
        if text_ids:
            # Upsert into text collection
            self.text_collection.upsert(
                ids=text_ids,
                documents=text_docs,
                metadatas=text_metadatas,
                embeddings=text_embeds
            )
            
        if vis_ids:
            # Upsert into visual collection
            self.visual_collection.upsert(
                ids=vis_ids,
                metadatas=vis_metadatas,
                embeddings=vis_embeds
            )
            
    def query_text(self, query_embedding: list[float], n_results: int, filter_dict: dict = None) -> list[dict]:
        where = filter_dict if filter_dict else None
        count = self.text_collection.count()
        if count == 0:
            return []
        safe_n = min(n_results, count)
        try:
            results = self.text_collection.query(
                query_embeddings=[query_embedding],
                n_results=safe_n,
                where=where,
                include=["documents", "metadatas", "distances"]
            )
            return self._format_results(results)
        except Exception as e:
            logger.error(f"Text collection query failed: {e}")
            return []

    def query_visual(self, query_embedding: list[float], n_results: int, filter_dict: dict = None) -> list[dict]:
        where = filter_dict if filter_dict else None
        count = self.visual_collection.count()
        if count == 0:
            return []
        safe_n = min(n_results, count)
        try:
            results = self.visual_collection.query(
                query_embeddings=[query_embedding],
                n_results=safe_n,
                where=where,
                include=["metadatas", "distances"]
            )
            return self._format_results(results, include_docs=False)
        except Exception as e:
            logger.error(f"Visual collection query failed: {e}")
            return []
        
    def _format_results(self, raw_results: dict, include_docs=True) -> list[dict]:
        if not raw_results or not raw_results["ids"] or not raw_results["ids"][0]:
            return []
            
        formatted = []
        for i in range(len(raw_results["ids"][0])):
            res = {
                "chunk_id": raw_results["ids"][0][i],
                "distance": raw_results["distances"][0][i],
                "metadata": raw_results["metadatas"][0][i]
            }
            if include_docs and "documents" in raw_results and raw_results["documents"]:
                res["text"] = raw_results["documents"][0][i]
            formatted.append(res)
        return formatted
        
    def delete_document(self, doc_id: str):
        self.text_collection.delete(where={"doc_id": doc_id})
        self.visual_collection.delete(where={"doc_id": doc_id})
