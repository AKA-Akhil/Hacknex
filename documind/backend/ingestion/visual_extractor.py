import fitz
from PIL import Image, ImageFilter
import io
from backend.config import CHART_CROPS_DIR
from backend.utils.helpers import setup_logger

logger = setup_logger(__name__)

def extract_visuals(page: fitz.Page, doc_id: str, page_num: int, table_bboxes: list) -> list:
    """Detects and extracts non-text visual regions from a page."""
    visuals = []
    try:
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            
            try:
                extracted_img = Image.open(io.BytesIO(image_bytes))
                width, height = extracted_img.size
                
                if width < 100 or height < 100:
                    continue
                    
                bboxes = page.get_image_bbox(xref)
                if not bboxes:
                    continue
                
                # Check overlap with tables
                is_in_table = False
                for tb in table_bboxes:
                    # tb: (x0, top, x1, bottom)
                    if (bboxes.x0 < tb[2] and bboxes.x1 > tb[0] and
                        bboxes.y0 < tb[3] and bboxes.y1 > tb[1]):
                        is_in_table = True
                        break
                
                if is_in_table:
                    continue
                
                img_filename = f"{doc_id}_page_{page_num}_visual_{img_index}.png"
                img_path = str(CHART_CROPS_DIR / img_filename)
                
                # Save the image
                extracted_img.save(img_path)
                
                visuals.append({
                    "image_path": img_path,
                    "bbox": (bboxes.x0, bboxes.y0, bboxes.x1, bboxes.y1)
                })
                
            except Exception as e:
                logger.warning(f"Failed to process embedded image {xref}: {e}")
                
    except Exception as e:
        logger.error(f"Error extracting visuals on page {page_num}: {e}", exc_info=True)
        
    return visuals
