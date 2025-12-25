from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from backend.services.pdf_processor import process_pdf
from backend.services.image_processor import process_image
from backend.utils.groq_client import send_to_groq

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No selected files'}), 400

    output_data = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            if filename.endswith('.pdf'):
                result = process_pdf(file_path)
            else:
                result = process_image(file_path)

            output_data.append(result)

            # Optionally send results to Groq
            send_to_groq(result)

    return jsonify({'results': output_data}), 200