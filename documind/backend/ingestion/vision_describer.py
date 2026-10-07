import time
import ollama
from backend.config import VISION_MODEL, VISION_PROMPT
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

def describe_visual(image_path: str) -> str:
    """Uses Ollama moondream to describe a visual region."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = ollama.chat(
                model=VISION_MODEL,
                messages=[{
                    "role": "user",
                    "content": VISION_PROMPT,
                    "images": [image_path]
                }]
            )
            return response.message.content
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Ollama vision call failed, retrying in {2**attempt}s... ({e})")
                time.sleep(2 ** attempt)
            else:
                logger.error(f"Vision model failed after {max_retries} attempts: {e}")
                return ""
    return ""
