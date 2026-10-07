import ollama
from backend.config import LLM_MODEL, SYSTEM_PROMPT
from backend.utils.helpers import setup_logger
import time

logger = setup_logger(__name__)

def generate(prompt: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """Generates an answer using the Ollama LLM."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = ollama.chat(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 1024,
                }
            )
            return response.message.content
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"LLM generation failed, retrying in {2**attempt}s... ({e})")
                time.sleep(2 ** attempt)
            else:
                logger.error(f"LLM failed after {max_retries} attempts: {e}")
                return "Error: Could not generate answer due to LLM failure."
    return ""
