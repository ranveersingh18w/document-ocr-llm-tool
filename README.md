# 🎯 Aadhaar Card Intelligent Document Processing

**A complete OCR + LLM pipeline for extracting structured data from Aadhaar cards**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-Latest-green.svg)](https://github.com/PaddlePaddle/PaddleOCR)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3-orange.svg)](https://groq.com/)

---

## 📋 Project Overview

This project implements an **end-to-end Intelligent Document Processing (IDP)** system for Aadhaar cards using:
- **PaddleOCR** for text extraction
- **Groq LLM (Llama 3.3 70B)** for structuring to json format

### ✨ Key Features

✅ **File Upload Interface** - Browse and select PDF or image files  
✅ **Multi-format Support** - PDF (multi-page) + Images (PNG, JPG, JPEG, BMP, TIFF)  
✅ **Advanced OCR** - PaddleOCR fast and best ocr engine
✅ **LLM Post-processing** - Understanding the content and formatting
✅ **Structured Output** - json file output
---

## 🎥 Screenshots

### Main Interface
![Main Interface](screenshots/main_interface.png)
*Upload interface with processing log and structured output panels*

### File Upload Dialog
![File Upload](screenshots/file_upload.png)
*Browse and select Aadhaar card PDF or image*

### Processing in Action
![Processing](screenshots/processing.png)
*Real-time OCR extraction with confidence scores*

### Structured JSON Output
![JSON Output](screenshots/json_output.png)
*Clean, structured data ready for downstream systems*

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12 (PaddleOCR requires Python 3.12)
- Windows/Linux/Mac

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Groq API Key (for LLM formatting)

**Windows:**
```powershell
$env:GROQ_API_KEY = "your-api-key-here"
```
---
## 💻 Usage

### Run the Application

```bash
python main.py
```

### Steps:
1. **Click "📂 Upload File"** button
2. **Select** your Aadhaar card (PDF or image)
3. **Watch** automatic processing
4. **View** structured JSON output
5. **Check** `output/` folder for saved results
---

## 📊 Output Format

```json
{
  "file_name": "aadhaar_card.pdf",
  "processed_at": "20251224_220530",
  "ocr_engine": "PaddleOCR",
  "llm_model": "Groq Llama 3.3 70B",
  "raw_text": "Government of India\nName: John Doe\n...",
  "extracted_fields": {
    "name": "John Doe",
    "aadhaar_number": "1234 5678 9012",
    "dob": "01/01/1990",
    "gender": "Male",
    "address": "123 Street, City, State - 500001",
    "father_name": "Father Name"
  }
}
```
---

## 🧠 Accuracy Improvement Strategy (NLP / LLM)

OCR output often contains noise such as spelling errors, broken lines and missing labels.

### Our Approach:

#### 1. **Reduce Noise**
- OCR results with confidence < 0.5 are discarded
- Reduces noise and improves data quality

#### 2. **Semantic Field Extraction using LLM**
- Raw OCR text is passed to Groq Llama 3.3 70B with prompts
- LLM understands context (e.g., name vs address)
- Handles variations like "DOB", "Date of Birth", "Birth Date"

#### 3. **Field Normalization**
- **Aadhaar Number**: Formatted as XXXX XXXX XXXX
- **Date**: Standardized format (DD/MM/YYYY)
- **Gender**: Normalized to Male/Female
- **Address**: Combined from multiple OCR lines

#### 4. **Fallback Condition**
- If LLM fails, raw OCR text is preserved for manual review
- ensures no data loss

### Why This Works:
This **hybrid OCR + LLM approach** significantly improves real-world document extraction accuracy compared to OCR alone by adding:
- Semantic understanding
- Context awareness  
- Error correction
- Field mapping intelligence

---

## 🏗️ Architecture

```
┌─────────────┐
│ PDF / Image │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  PaddleOCR      │ ← Text Extraction
│  (Confidence    │   (Multi-page PDF support)
│   Filtering)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Raw OCR Text   │
│  (with scores)  │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Groq LLM       │ ← Semantic Understanding
│  (Llama 3.3)    │   Field Extraction
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Structured JSON │ ← Final Output
│  (Auto-saved)   │
└─────────────────┘
```

---

## 📁 Project Structure

```
final_code/
├── main.py              # Main application (GUI + OCR + LLM)
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── SCREENSHOT_GUIDE.md # How to capture screenshots
└── output/             # Auto-created for results
    └── aadhaar_*.json  # Extracted data files
```

## 📧 Contact

**Project by:** [Your Name]  
**Email:** [Your Email]  
**Submitted for:** Intelligent Document Processing Screening Task

