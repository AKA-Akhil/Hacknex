import pytesseract
from pytesseract import Output
from PIL import Image
from backend.config import TESSERACT_CONFIG, OCR_CONFIDENCE_THRESHOLD
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

def ocr_page(image: Image.Image) -> tuple[str, float]:
    """Runs OCR on an image and returns (text, average_confidence)."""
    try:
        text = pytesseract.image_to_string(image, config=TESSERACT_CONFIG)
        data = pytesseract.image_to_data(image, output_type=Output.DICT)
        
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        
        return text, avg_conf
    except Exception as e:
        logger.error(f"OCR failed: {e}", exc_info=True)
        return "", 0.0

def is_scanned_page(text: str) -> bool:
    """Heuristic to check if a page is likely scanned based on PyMuPDF text length."""
    if not text:
        return True
    
    # Strip whitespace and check length
    cleaned = text.strip()
    return len(cleaned) < 50
