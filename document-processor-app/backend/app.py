from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.upload import upload_bp
import os
from config import Config

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

app.register_blueprint(upload_bp, url_prefix='/api')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)