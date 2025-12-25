import os

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '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')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'outputs/')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # Limit upload size to 100 MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS