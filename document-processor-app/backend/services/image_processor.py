from PIL import Image
import pytesseract
import os

def process_image(file_path):
    """Extract text from image using Tesseract OCR"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    try:
        # Open and verify image
        img = Image.open(file_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Use Tesseract to extract text
        extracted_text = pytesseract.image_to_string(img)
        
        return extracted_text.strip() if extracted_text.strip() else "No text detected in image"
        
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")