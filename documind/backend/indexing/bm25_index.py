import pickle
import os
from rank_bm25 import BM25Okapi
from backend.config import STORAGE_DIR
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

class BM25Index:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BM25Index, cls).__new__(cls)
            cls._instance.index_path = STORAGE_DIR / "bm25_index.pkl"
            cls._instance.tokenized_corpus = []
            cls._instance.chunk_metadata = []
            cls._instance.bm25 = None
            cls._instance._load()
        return cls._instance
        
    def _tokenize(self, text: str) -> list[str]:
        return text.lower().split()
        
    def _load(self):
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'rb') as f:
                    data = pickle.load(f)
                    self.tokenized_corpus = data.get("corpus", [])
                    self.chunk_metadata = data.get("metadata", [])
                
                if self.tokenized_corpus:
                    self.bm25 = BM25Okapi(self.tokenized_corpus)
                logger.info(f"Loaded BM25 index with {len(self.tokenized_corpus)} chunks.")
            except Exception as e:
                logger.error(f"Failed to load BM25 index: {e}")
                
    def _save(self):
        try:
            with open(self.index_path, 'wb') as f:
                pickle.dump({
                    "corpus": self.tokenized_corpus,
                    "metadata": self.chunk_metadata
                }, f)
        except Exception as e:
            logger.error(f"Failed to save BM25 index: {e}")
            
    def add_chunks(self, chunks: list):
        if not chunks:
            return
            
        for chunk in chunks:
            tokens = self._tokenize(chunk.text)
            self.tokenized_corpus.append(tokens)
            
            meta = {
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "doc_name": chunk.doc_name,
                "page_number": chunk.page_number,
                "content_type": chunk.content_type,
                "image_path": chunk.image_path if chunk.image_path else "",
                "text": chunk.text
            }
            self.chunk_metadata.append(meta)
            
        # Rebuild index
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self._save()
        
    def query(self, query_text: str, top_k: int) -> list[tuple[str, float]]:
        if not self.bm25 or not self.tokenized_corpus:
            return []
            
        tokenized_query = self._tokenize(query_text)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append((self.chunk_metadata[idx]["chunk_id"], scores[idx]))
                
        return results
        
    def delete_document(self, doc_id: str):
        # Filter out chunks for this doc_id
        filtered_corpus = []
        filtered_meta = []
        
        for i, meta in enumerate(self.chunk_metadata):
            if meta.get("doc_id") != doc_id:
                filtered_corpus.append(self.tokenized_corpus[i])
                filtered_meta.append(meta)
                
        self.tokenized_corpus = filtered_corpus
        self.chunk_metadata = filtered_meta
        
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
        else:
            self.bm25 = None
            
        self._save()
        
    def get_chunk_by_id(self, chunk_id: str) -> dict:
        for meta in self.chunk_metadata:
            if meta["chunk_id"] == chunk_id:
                return meta
        return None
