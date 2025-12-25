from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from services.pdf_processor import process_pdf
from services.image_processor import process_image
from utils.groq_client import format_with_groq

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400

        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400

        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Save uploaded file
                file.save(file_path)
                
                try:
                    # Process based on file type
                    if filename.lower().endswith('.pdf'):
                        extracted_text = process_pdf(file_path)
                    else:
                        extracted_text = process_image(file_path)
                    
                    # Format with Groq LLM
                    formatted_data = format_with_groq(extracted_text)
                    
                    # Save output
                    output_filename = f"{timestamp}_{os.path.splitext(filename)[0]}_output.json"
                    output_path = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
                    
                    results.append({
                        'filename': filename,
                        'status': 'success',
                        'extracted_text': extracted_text,
                        'formatted_data': formatted_data,
                        'output_file': output_filename
                    })
                    
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'status': 'error',
                        'error': str(e)
                    })
                
                # Clean up uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)
            else:
                results.append({
                    'filename': file.filename,
                    'status': 'error',
                    'error': 'File type not allowed'
                })

        return jsonify({
            'success': True,
            'results': results,
            'total_files': len(files),
            'processed': len([r for r in results if r['status'] == 'success'])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Document Processor API is running'}), 200