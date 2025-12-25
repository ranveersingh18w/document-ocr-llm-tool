from PIL import Image
from paddleocr import PaddleOCR
import os

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

def process_image(file_path):
    """Extract text from image using PaddleOCR"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        # Open and verify image
        img = Image.open(file_path)
        img.verify()
        
        # Reopen for processing (verify closes the file)
        img = Image.open(file_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Use PaddleOCR to extract text
        result = ocr.ocr(file_path, cls=True)
        
        extracted_text = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]  # Extract text
                confidence = line[1][1]  # Extract confidence
                extracted_text.append(text)
        
        return '\n'.join(extracted_text) if extracted_text else "No text detected in image"
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")