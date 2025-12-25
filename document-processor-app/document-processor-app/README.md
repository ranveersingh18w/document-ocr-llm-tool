# Document Processor App

## Overview
The Document Processor App is a web application that allows users to upload multiple files, including PDFs and images, for processing. The application features a user-friendly interface and a robust backend powered by Python and Flask. It utilizes the Groq API for advanced processing capabilities.

## Project Structure
```
document-processor-app
├── frontend
│   ├── index.html          # Main HTML entry point
│   ├── css
│   │   └── styles.css      # Styles for the frontend
│   ├── js
│   │   ├── app.js          # Main JavaScript logic
│   │   └── fileUpload.js    # File upload functionality
│   └── assets
│       └── .gitkeep        # Keeps the assets directory in Git
├── backend
│   ├── app.py              # Main entry point for the backend
│   ├── requirements.txt     # Python dependencies
│   ├── config.py           # Configuration settings
│   ├── routes
│   │   ├── __init__.py     # Initializes routes package
│   │   └── upload.py       # Handles file uploads
│   ├── services
│   │   ├── __init__.py     # Initializes services package
│   │   ├── pdf_processor.py # PDF processing functions
│   │   └── image_processor.py # Image processing functions
│   └── utils
│       ├── __init__.py     # Initializes utils package
│       └── groq_client.py   # Interacts with the Groq API
├── uploads
│   └── .gitkeep            # Keeps the uploads directory in Git
├── outputs
│   └── .gitkeep            # Keeps the outputs directory in Git
├── .env                     # Environment variables
├── .gitignore               # Files to ignore by Git
├── render.yaml              # Deployment configuration for Render
└── README.md                # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd document-processor-app
   ```

2. **Install dependencies:**
   Navigate to the `backend` directory and install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Groq API key and any other necessary environment variables.

4. **Run the backend:**
   Start the Flask application:
   ```
   python backend/app.py
   ```

5. **Access the frontend:**
   Open `frontend/index.html` in your web browser to interact with the application.

## Usage
- Users can upload multiple PDF and image files through the frontend interface.
- The backend processes the uploaded files and returns the results dynamically.
- Users can click on the processed files to view the output.

## Deployment
To deploy the application to Render, use the Render CLI and follow the instructions in the `render.yaml` file.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.