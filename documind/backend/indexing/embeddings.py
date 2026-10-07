from sentence_transformers import SentenceTransformer
import open_clip
import torch
from PIL import Image
from backend.config import TEXT_EMBED_MODEL, CLIP_MODEL_NAME, CLIP_PRETRAINED
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

class TextEmbedder:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextEmbedder, cls).__new__(cls)
            logger.info(f"Loading Text Embedder ({TEXT_EMBED_MODEL}) on CPU...")
            cls._instance.model = SentenceTransformer(TEXT_EMBED_MODEL, device="cpu")
        return cls._instance
        
    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
        
    def embed_query(self, query: str) -> list[float]:
        return self.model.encode([query], convert_to_numpy=True)[0].tolist()

class ImageEmbedder:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageEmbedder, cls).__new__(cls)
            logger.info(f"Loading CLIP ({CLIP_MODEL_NAME}) on CPU...")
            model, _, preprocess = open_clip.create_model_and_transforms(CLIP_MODEL_NAME, pretrained=CLIP_PRETRAINED)
            cls._instance.model = model
            cls._instance.preprocess = preprocess
            cls._instance.tokenizer = open_clip.get_tokenizer(CLIP_MODEL_NAME)
        return cls._instance
        
    def embed_image(self, image_path: str) -> list[float]:
        try:
            image = Image.open(image_path).convert("RGB")
            image_input = self.preprocess(image).unsqueeze(0)
            with torch.no_grad():
                image_features = self.model.encode_image(image_input)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            return image_features[0].tolist()
        except Exception as e:
            logger.error(f"Error embedding image {image_path}: {e}")
            return []
            
    def embed_text(self, text: str) -> list[float]:
        text_input = self.tokenizer([text])
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features[0].tolist()
