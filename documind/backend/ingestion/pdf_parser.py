import fitz
import io
from PIL import Image
from backend.config import PAGE_IMAGES_DIR
from backend.utils.helpers import setup_logger, generate_id
from backend.ingestion.ocr_handler import ocr_page, is_scanned_page
from backend.ingestion.table_extractor import extract_tables
from backend.ingestion.visual_extractor import extract_visuals
from backend.ingestion.vision_describer import describe_visual

logger = setup_logger(__name__)

class ContentBlock:
    def __init__(self, block_id, doc_id, doc_name, page_number, content_type, content, image_path=None, bbox=None, metadata=None):
        self.block_id = block_id
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.page_number = page_number
        self.content_type = content_type
        self.content = content
        self.image_path = image_path
        self.bbox = bbox
        self.metadata = metadata or {}

def parse_pdf(pdf_path: str, doc_id: str, doc_name: str) -> list[ContentBlock]:
    """Extracts text, tables, and visuals from a PDF and returns a list of ContentBlocks."""
    blocks = []
    
    try:
        # Extract tables for the whole document first
        tables_per_page = {}
        all_tables = extract_tables(pdf_path)
        for t in all_tables:
            p_num = t["page_number"]
            if p_num not in tables_per_page:
                tables_per_page[p_num] = []
            tables_per_page[p_num].append(t)
            
            blocks.append(ContentBlock(
                block_id=generate_id(),
                doc_id=doc_id,
                doc_name=doc_name,
                page_number=p_num,
                content_type="table",
                content=t["markdown"],
                bbox=t["bbox"],
                metadata={"raw_data": t["raw_data"]}
            ))
            
        with fitz.open(pdf_path) as doc:
            for page_index, page in enumerate(doc):
                page_num = page_index + 1
                
                # Render page as image (2x resolution)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                page_image = Image.open(io.BytesIO(img_data))
                
                # Save rendered page
                page_img_path = str(PAGE_IMAGES_DIR / f"{doc_id}_page_{page_num}.png")
                page_image.save(page_img_path)
                
                # Extract Text
                text = page.get_text("text")
                if is_scanned_page(text):
                    logger.info(f"Page {page_num} seems scanned. Running OCR.")
                    text, conf = ocr_page(page_image)
                    metadata = {"ocr_confidence": conf}
                else:
                    metadata = {}
                    
                if text.strip():
                    blocks.append(ContentBlock(
                        block_id=generate_id(),
                        doc_id=doc_id,
                        doc_name=doc_name,
                        page_number=page_num,
                        content_type="text",
                        content=text.strip(),
                        metadata=metadata
                    ))
                
                # Extract Visuals
                table_bboxes = [t["bbox"] for t in tables_per_page.get(page_num, [])]
                visuals = extract_visuals(page, doc_id, page_num, table_bboxes)
                
                for vis in visuals:
                    description = describe_visual(vis["image_path"])
                    blocks.append(ContentBlock(
                        block_id=generate_id(),
                        doc_id=doc_id,
                        doc_name=doc_name,
                        page_number=page_num,
                        content_type="chart",
                        content=description,
                        image_path=vis["image_path"],
                        bbox=vis["bbox"]
                    ))
                    
    except Exception as e:
        logger.error(f"Failed to parse PDF {pdf_path}: {e}", exc_info=True)
        
    return blocks
