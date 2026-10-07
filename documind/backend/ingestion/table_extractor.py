import pdfplumber
from backend.config import MIN_TABLE_ROWS, MIN_TABLE_COLS
from backend.utils.helpers import setup_logger
from typing import List, Dict, Any

logger = setup_logger(__name__)

def extract_tables(pdf_path: str) -> List[Dict[str, Any]]:
    """Extracts tables from a PDF using pdfplumber and returns them in structured format."""
    extracted_tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # find_tables returns Table objects with bbox
                tables = page.find_tables()
                
                for table in tables:
                    data = table.extract()
                    if not data:
                        continue
                        
                    # Filter by minimum rows and cols
                    if len(data) < MIN_TABLE_ROWS or len(data[0]) < MIN_TABLE_COLS:
                        continue
                        
                    # Convert to Markdown
                    markdown_rows = []
                    for i, row in enumerate(data):
                        # Clean up None values and newlines in cells
                        cleaned_row = [str(cell).replace("\n", " ") if cell is not None else "" for cell in row]
                        row_str = "| " + " | ".join(cleaned_row) + " |"
                        markdown_rows.append(row_str)
                        
                        # Add separator after header
                        if i == 0:
                            sep_row = "|-" + "-|-".join(["-" * len(c) for c in cleaned_row]) + "-|"
                            markdown_rows.append(sep_row)
                            
                    markdown_str = "\n".join(markdown_rows)
                    
                    extracted_tables.append({
                        "page_number": page_num,
                        "raw_data": data,
                        "markdown": markdown_str,
                        "bbox": table.bbox  # (x0, top, x1, bottom)
                    })
    except Exception as e:
        logger.error(f"Error extracting tables from {pdf_path}: {e}", exc_info=True)
        
    return extracted_tables
