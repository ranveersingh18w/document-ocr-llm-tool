import os
import json
from datetime import datetime
from paddleocr import PaddleOCR
from groq import Groq
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
import fitz  # PyMuPDF for PDF handling

class AadhaarOCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aadhaar Card OCR Extractor - Upload & Extract")
        self.root.geometry("1200x700")
        
        # Get Groq API Key from environment
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.ocr = None
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🎯 Aadhaar Card OCR Extractor", 
                        font=("Arial", 20, "bold"), bg="#2C3E50", fg="white", pady=15)
        title.pack(fill=tk.X)
        
        # Info bar
        info_frame = tk.Frame(self.root, bg="#34495E", pady=10)
        info_frame.pack(fill=tk.X)
        
        tk.Label(info_frame, text="📄 Upload PDF/Image", 
                font=("Arial", 10), bg="#34495E", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text="🔍 PaddleOCR Extraction", 
                font=("Arial", 10), bg="#34495E", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text="🤖 LLM Formatting", 
                font=("Arial", 10), bg="#34495E", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text="💾 JSON Output", 
                font=("Arial", 10), bg="#34495E", fg="white").pack(side=tk.LEFT, padx=20)
        
        # Button Frame
        btn_frame = tk.Frame(self.root, pady=15, bg="#ECF0F1")
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="📂 Upload File (PDF/Image)", command=self.upload_file,
                 font=("Arial", 13, "bold"), bg="#27AE60", fg="white", 
                 padx=30, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=20)
        
        tk.Button(btn_frame, text="🗑️ Clear", command=self.clear_all,
                 font=("Arial", 12), bg="#E74C3C", fg="white", 
                 padx=25, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="📁 Open Output Folder", command=self.open_output_folder,
                 font=("Arial", 12), bg="#3498DB", fg="white", 
                 padx=25, pady=10, cursor="hand2").pack(side=tk.LEFT, padx=5)
        
        # File info label
        self.file_label = tk.Label(btn_frame, text="No file selected", 
                                   font=("Arial", 10, "italic"), bg="#ECF0F1", fg="#7F8C8D")
        self.file_label.pack(side=tk.LEFT, padx=20)
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg="#ECF0F1")
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', length=400)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.progress_label = tk.Label(progress_frame, text="Ready", 
                                      font=("Arial", 10, "bold"), bg="#ECF0F1")
        self.progress_label.pack(side=tk.LEFT)
        
        # Main content area - 2 columns
        content_frame = tk.Frame(self.root, bg="#ECF0F1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Left: Processing Log
        left_frame = tk.LabelFrame(content_frame, text="📊 Processing Log", 
                                   font=("Arial", 11, "bold"), bg="#ECF0F1")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, 
                                                  font=("Consolas", 9), height=25)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right: Extracted Data
        right_frame = tk.LabelFrame(content_frame, text="📝 Extracted Data (JSON)", 
                                    font=("Arial", 11, "bold"), bg="#ECF0F1")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                     font=("Consolas", 10), height=25)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        self.status = tk.Label(self.root, text="Ready | Upload a file to start", 
                              relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9), bg="#BDC3C7")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def upload_file(self):
        """Open file dialog to upload PDF or image"""
        file_path = filedialog.askopenfilename(
            title="Select Aadhaar Card (PDF/Image)",
            filetypes=[
                ("All Supported", "*.pdf *.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.clear_all()
            
            # Process in background thread
            thread = threading.Thread(target=self.process_file, args=(file_path,))
            thread.daemon = True
            thread.start()
    
    def initialize_ocr(self):
        """Initialize PaddleOCR if not already initialized"""
        if self.ocr is None:
            self.log("🔄 Initializing PaddleOCR (first time only)...")
            self.ocr = PaddleOCR(use_textline_orientation=True, lang='en')
            self.log("✅ PaddleOCR initialized!\n")
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF by converting pages to images"""
        self.initialize_ocr()
        all_text = []
        
        self.log(f"📄 Opening PDF: {os.path.basename(pdf_path)}")
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        
        self.log(f"📑 Found {total_pages} page(s)\n")
        
        for page_num in range(total_pages):
            self.log(f"🔍 Processing page {page_num + 1}/{total_pages}...")
            
            page = pdf_document[page_num]
            mat = fitz.Matrix(300/72, 300/72)  # 300 DPI
            pix = page.get_pixmap(matrix=mat)
            
            temp_image = f"temp_page_{page_num}.png"
            pix.save(temp_image)
            
            try:
                # Run OCR on the page image
                result = self.ocr.predict(input=temp_image)
                
                # Extract text from result
                page_text_lines = []
                for page_result in result:
                    # Access the JSON structure
                    if hasattr(page_result, 'json'):
                        json_data = page_result.json
                        if 'res' in json_data and 'rec_texts' in json_data['res']:
                            rec_texts = json_data['res']['rec_texts']
                            rec_scores = json_data['res'].get('rec_scores', [])
                            
                            for idx, text in enumerate(rec_texts):
                                score = rec_scores[idx] if idx < len(rec_scores) else 1.0
                                if score > 0.5:  # Filter low confidence
                                    page_text_lines.append(text)
                                    self.log(f"  ✓ '{text}' (confidence: {score:.2f})")
                
                page_text = '\n'.join(page_text_lines)
                all_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
            finally:
                # Clean up temp file
                if os.path.exists(temp_image):
                    try:
                        os.remove(temp_image)
                    except:
                        pass
        
        pdf_document.close()
        return '\n\n'.join(all_text)
    
    def extract_text_from_image(self, image_path):
        """Extract text from image using PaddleOCR"""
        self.initialize_ocr()
        
        self.log(f"🖼️ Processing image: {os.path.basename(image_path)}")
        result = self.ocr.predict(input=image_path)
        
        # Extract text from result
        extracted_lines = []
        for page_result in result:
            if hasattr(page_result, 'json'):
                json_data = page_result.json
                if 'res' in json_data and 'rec_texts' in json_data['res']:
                    rec_texts = json_data['res']['rec_texts']
                    rec_scores = json_data['res'].get('rec_scores', [])
                    
                    for idx, text in enumerate(rec_texts):
                        score = rec_scores[idx] if idx < len(rec_scores) else 1.0
                        if score > 0.5:
                            extracted_lines.append(text)
                            self.log(f"  ✓ '{text}' (confidence: {score:.2f})")
        
        return '\n'.join(extracted_lines)
    
    def format_with_llm(self, raw_text):
        """Use Groq LLM to format raw text into structured JSON for Aadhaar card"""
        if not self.groq_api_key:
            return None, "No Groq API key provided"
        
        groq_client = Groq(api_key=self.groq_api_key)
        
        prompt = f"""You are an expert data extraction assistant. Extract information from the following Aadhaar card text and return ONLY a valid JSON object.

Raw Text:
{raw_text}

Extract these fields (if present):
- name (full name)
- aadhaar_number (12-digit number, format: XXXX XXXX XXXX)
- dob (date of birth)
- gender (Male/Female)
- address (complete address)
- father_name (if mentioned)
- year_of_birth (if mentioned)
- phone (if mentioned)
- any other relevant fields you find

Return ONLY valid JSON, no explanations or markdown. Format:
{{
  "name": "...",
  "aadhaar_number": "...",
  "dob": "...",
  "gender": "...",
  "address": "...",
  "father_name": "..."
}}"""

        try:
            self.log("\n🤖 Formatting with Groq LLM...")
            
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_completion_tokens=2048,
                top_p=1,
                stream=True,
                stop=None
            )
            
            full_response = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                full_response += content
            
            # Clean response
            full_response = full_response.strip()
            if full_response.startswith("```json"):
                full_response = full_response[7:]
            if full_response.startswith("```"):
                full_response = full_response[3:]
            if full_response.endswith("```"):
                full_response = full_response[:-3]
            
            structured_data = json.loads(full_response.strip())
            return structured_data, None
            
        except Exception as e:
            return None, f"LLM error: {str(e)}"
    
    def process_file(self, file_path):
        """Process uploaded file"""
        try:
            self.status.config(text=f"Processing: {os.path.basename(file_path)}")
            self.progress_bar.start(10)
            self.progress_label.config(text="Processing...")
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            self.log("=" * 70)
            self.log(f"📁 File: {os.path.basename(file_path)}")
            self.log(f"📏 Type: {file_ext}")
            self.log("=" * 70)
            self.log("\n🔍 Stage 1: Text Extraction with PaddleOCR\n")
            
            # Extract text based on file type
            if file_ext == '.pdf':
                raw_text = self.extract_text_from_pdf(file_path)
            elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
                raw_text = self.extract_text_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")
            
            self.log(f"\n📄 Raw Extracted Text:")
            self.log("-" * 70)
            self.log(raw_text if raw_text else "(No text extracted)")
            self.log("-" * 70)
            
            if not raw_text or len(raw_text.strip()) < 10:
                self.log("\n❌ No significant text extracted!")
                self.status.config(text="Failed: No text extracted")
                self.progress_bar.stop()
                self.progress_label.config(text="Failed")
                return
            
            # Stage 2: Format with LLM
            self.log("\n🤖 Stage 2: Formatting with LLM\n")
            structured_data, error = self.format_with_llm(raw_text)
            
            if error:
                self.log(f"⚠️  LLM formatting failed: {error}")
                structured_data = {"raw_text": raw_text}
            else:
                self.log("✅ LLM Formatting successful!")
            
            # Display structured data
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "📊 EXTRACTED AADHAAR CARD DATA\n")
            self.result_text.insert(tk.END, "=" * 70 + "\n\n")
            self.result_text.insert(tk.END, json.dumps(structured_data, ensure_ascii=False, indent=2))
            self.result_text.insert(tk.END, "\n\n" + "=" * 70)
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = os.path.basename(file_path)
            
            output_data = {
                "file_name": file_name,
                "file_path": os.path.abspath(file_path),
                "processed_at": timestamp,
                "ocr_engine": "PaddleOCR",
                "llm_model": "Groq Llama 3.3 70B" if not error else "None",
                "raw_text": raw_text,
                "extracted_fields": structured_data
            }
            
            output_file = os.path.join(
                self.output_dir,
                f"aadhaar_{os.path.splitext(file_name)[0]}_{timestamp}.json"
            )
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            self.log(f"\n💾 Saved to: {output_file}")
            self.log("\n✅ Processing completed successfully!")
            
            self.status.config(text=f"✅ Success! Saved to: {os.path.basename(output_file)}")
            self.progress_label.config(text="Completed!")
            
            messagebox.showinfo("Success!", 
                              f"Aadhaar card processed successfully!\n\n"
                              f"Output saved to:\n{output_file}")
            
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            self.status.config(text=f"Error: {str(e)}")
            messagebox.showerror("Error", f"Processing failed:\n{str(e)}")
        
        finally:
            self.progress_bar.stop()
            if self.progress_label.cget("text") != "Completed!":
                self.progress_label.config(text="Ready")
    
    def clear_all(self):
        """Clear all text areas"""
        self.log_text.delete(1.0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.status.config(text="Ready | Upload a file to start")
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        import subprocess
        output_path = os.path.abspath(self.output_dir)
        subprocess.Popen(f'explorer "{output_path}"')


if __name__ == "__main__":
    root = tk.Tk()
    app = AadhaarOCRApp(root)
    root.mainloop()
