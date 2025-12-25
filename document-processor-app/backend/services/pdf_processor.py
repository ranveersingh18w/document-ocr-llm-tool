import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import os
from PIL import Image
import io

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

def process_pdf(file_path):
    """Extract text from PDF using PyMuPDF and PaddleOCR for images"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    all_text = []
    
    try:
        pdf_document = fitz.open(file_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Extract text directly
            text = page.get_text()
            
            # If no text found, use OCR on the page image
            if not text.strip():
                # Render page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
                img_data = pix.tobytes("png")
                
                # Use PaddleOCR
                result = ocr.ocr(img_data, cls=True)
                if result and result[0]:
                    text = '\n'.join([line[1][0] for line in result[0]])
            
            all_text.append(f"--- Page {page_num + 1} ---\n{text}")
        
        pdf_document.close()
        return '\n\n'.join(all_text)
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")