# Document OCR & AI Processor

A powerful web application that processes PDFs and images using OCR (PaddleOCR) and formats the extracted data using AI (Groq LLM).

## Features

- 📄 **Multi-file Upload**: Upload multiple PDFs and images (up to 100 files)
- 🔍 **Advanced OCR**: Extract text from documents using PaddleOCR
- 🤖 **AI Formatting**: Structure extracted data using Groq's LLM
- 💾 **JSON Export**: Download formatted data as JSON
- 🎨 **Beautiful UI**: Modern, responsive interface with drag-and-drop
- ⚡ **Real-time Progress**: Track processing status for each file

## Tech Stack

### Backend
- Python 3.11
- Flask (Web Framework)
- PaddleOCR (OCR Engine)
- PyMuPDF (PDF Processing)
- Groq API (LLM for data formatting)

### Frontend
- HTML5
- CSS3 (Modern responsive design)
- Vanilla JavaScript
- Font Awesome Icons

## Local Development

### Prerequisites
- Python 3.11+
- Git

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd document-ocr---llm-tool-project
```

2. Navigate to backend directory:
```bash
cd document-processor-app/backend
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Deployment to Render

### Method 1: Using Render Dashboard

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New +" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file
6. Click "Apply" to deploy

### Method 2: Using Render CLI (Not Recommended - Use Dashboard Instead)

The Render CLI is primarily for managing existing services. It's recommended to use the dashboard for initial deployment.

## Environment Variables

The following environment variables are configured in `render.yaml`:

- `GROQ_API_KEY`: Your Groq API key (already set)
- `PYTHON_VERSION`: 3.11.0
- `PORT`: 10000 (automatically set by Render)

## API Endpoints

- `GET /` - Serve frontend application
- `POST /api/upload` - Upload and process files
- `GET /api/health` - Health check endpoint

## File Support

Supported file types:
- PDF (.pdf)
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)

Maximum file size: 100MB per file

## Usage

1. **Upload Files**: Drag and drop or click to select files
2. **Review**: See the list of selected files
3. **Process**: Click "Process Documents" button
4. **View Results**: Click on any result card to view details
5. **Download**: Export formatted data as JSON

## Project Structure

```
document-processor-app/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   └── upload.py       # Upload endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py    # PDF processing
│   │   └── image_processor.py  # Image processing
│   └── utils/
│       ├── __init__.py
│       └── groq_client.py      # Groq API integration
├── frontend/
│   ├── index.html          # Main HTML
│   ├── css/
│   │   └── styles.css      # Styles
│   └── js/
│       ├── app.js          # Main application logic
│       └── fileUpload.js   # File upload utilities
├── uploads/                # Temporary upload folder
├── outputs/                # Processed outputs
└── render.yaml             # Render deployment config
```

## Features in Detail

### OCR Processing
- Uses PaddleOCR for accurate text extraction
- Supports multiple languages
- Handles both typed and handwritten text
- Processes scanned documents and images

### AI Formatting
- Groq's LLaMA 3.3 70B model
- Structures unstructured text into JSON
- Extracts entities and relationships
- Identifies document types automatically

### User Interface
- Responsive design works on all devices
- Drag-and-drop file upload
- Real-time progress tracking
- Modal viewer for detailed results
- Copy to clipboard functionality
- One-click JSON download

## Performance

- Processes multiple files concurrently
- Optimized for batch processing
- Automatic cleanup of temporary files
- Memory-efficient streaming

## Security

- File type validation
- File size limits
- Secure file handling
- CORS enabled for API access

## Troubleshooting

### PaddleOCR Installation Issues
If you encounter issues with PaddleOCR:
```bash
pip install paddlepaddle-gpu  # For GPU support
# OR
pip install paddlepaddle      # CPU only
```

### Groq API Issues
- Verify your API key is correct
- Check your Groq account quota
- Ensure you have internet connectivity

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions, please open an issue on GitHub.

## Acknowledgments

- PaddleOCR for the amazing OCR engine
- Groq for fast LLM inference
- Render for easy deployment
- Font Awesome for icons

---

Made with ❤️ using PaddleOCR & Groq AI
