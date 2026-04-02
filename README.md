# OCR Web Application

A modern web-based OCR (Optical Character Recognition) application that extracts text from images and PDF files using Tesseract OCR engine. Built with FastAPI, Python, and Docker.

!![OCR Web Application Screenshot ](DrawGen.png)

## Features

- **Multi-format Support**: Process JPG, JPEG, PNG, BMP, TIFF, GIF images and PDF documents
- **Multi-language OCR**: Auto-detection and support for English, Turkish, Russian, Spanish
- **Modern Web Interface**: Dark-themed, responsive UI with drag-and-drop file upload
- **Batch Processing**: Upload and process multiple files simultaneously
- **RESTful API**: Clean API endpoints for integration with other applications
- **Dockerized**: Easy deployment with Docker and Docker Compose
- **Real-time Processing**: Fast text extraction with progress indication

## Tech Stack

- **Backend**: FastAPI, Python 3.10
- **OCR Engine**: Tesseract OCR with language packs
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PDF Processing**: pdf2image, poppler-utils
- **Image Processing**: Pillow (PIL)
- **Containerization**: Docker
- **Server**: Uvicorn ASGI server

## Project Structure

```
ocr-webapp/
├── app/
│   ├── main.py              # FastAPI application and endpoints
│   ├── ocr_utils.py         # OCR utility functions
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Docker configuration
│   └── static/
│       └── index.html      # Web interface
├── README.md               # This file
└── ocr-webapp_2.0.tar     # Docker image archive (optional)
```

## Quick Start

### Using Docker (Recommended)

1. **Pull or build the Docker image:**

   ```bash
   # Option 1: Build from source
   cd ocr-webapp
   docker build -t ocr-webapp:latest ./app
   
   # Option 2: Load from archive (if available)
   docker load -i ocr-webapp_2.0.tar
   ```

2. **Run the container:**

   ```bash
   docker run -d -p 7346:7346 --name ocr-app ocr-webapp:latest
   ```

3. **Access the application:**
   - Web Interface: http://localhost:7346/static
   - API Health Check: http://localhost:7346/api/health

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  ocr-webapp:
    build: ./app
    container_name: ocr-webapp
    ports:
      - "7346:7346"
    restart: unless-stopped
    volumes:
      - ./uploads:/app/uploads  # Optional: for file persistence
```

Then run:
```bash
docker-compose up -d
```

### Manual Installation

1. **Install system dependencies:**

   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y tesseract-ocr \
       tesseract-ocr-tur tesseract-ocr-rus \
       tesseract-ocr-eng tesseract-ocr-spa \
       libtesseract-dev poppler-utils
   
   # macOS (using Homebrew)
   brew install tesseract poppler
   ```

2. **Install Python dependencies:**

   ```bash
   cd app
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   cd app
   uvicorn main:app --host 0.0.0.0 --port 7346 --reload
   ```

## Usage

### Web Interface

1. Navigate to `http://localhost:7346/static`
2. Drag and drop files or click to browse
3. Select OCR language (Auto, English, Turkish, Russian, Spanish)
4. Click "Extract Text"
5. View extracted text in the right panel

### API Endpoints

#### POST `/api/upload`
Upload files for OCR processing.

**Request:**
- `multipart/form-data` with:
  - `files`: One or more image/PDF files
  - `language`: Language code (`auto`, `en`, `tr`, `ru`, `es`)

**Response:**
```json
{
  "results": [
    {
      "filename": "document.pdf",
      "date": "2024-01-01 12:34:56",
      "language": "auto",
      "status": "done",
      "text": "Extracted text content..."
    }
  ]
}
```

#### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## API Examples

### Using cURL

```bash
curl -X POST http://localhost:7346/api/upload \
  -F "files=@image.jpg" \
  -F "files=@document.pdf" \
  -F "language=en"
```

### Using Python

```python
import requests

files = [
    ('files', ('image.jpg', open('image.jpg', 'rb'), 'image/jpeg')),
    ('files', ('document.pdf', open('document.pdf', 'rb'), 'application/pdf'))
]
data = {'language': 'en'}

response = requests.post('http://localhost:7346/api/upload', files=files, data=data)
print(response.json())
```

## Configuration

### Environment Variables

The application can be configured using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 7346 | Port to run the server on |
| `HOST` | 0.0.0.0 | Host to bind the server to |
| `TESSERACT_PATH` | (system) | Path to Tesseract executable |
| `LOG_LEVEL` | INFO | Logging level |

### Language Support

The application supports the following languages out of the box:

| Language | Code | Tesseract Language Pack |
|----------|------|-------------------------|
| Auto (English) | `auto` | eng |
| English | `en` | eng |
| Turkish | `tr` | tur |
| Russian | `ru` | rus |
| Spanish | `es` | spa |

To add more languages, install additional Tesseract language packs and update the `SUPPORTED_LANGUAGES` dictionary in `app/main.py`.

## Development

### Prerequisites

- Python 3.10+
- Tesseract OCR 4.0+
- Docker and Docker Compose (optional)

### Setting Up Development Environment

1. **Clone and setup:**

   ```bash
   git clone <repository-url>
   cd ocr-webapp
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   cd app
   pip install -r requirements.txt
   ```

2. **Run in development mode:**

   ```bash
   cd app
   uvicorn main:app --host 0.0.0.0 --port 7346 --reload
   ```

3. **Run tests:**
   *(Add tests as needed)*

### Building Docker Image

```bash
cd app
docker build -t ocr-webapp:dev .
```

### Extending the Application

- **Add new file formats**: Update `is_image_file()` and `is_pdf_file()` functions in `ocr_utils.py`
- **Add languages**: Install Tesseract language packs and update `SUPPORTED_LANGUAGES` in `main.py`
- **Modify UI**: Edit `app/static/index.html` and associated CSS/JS
- **Add authentication**: Implement FastAPI middleware for API security

## Deployment

### Production Considerations

1. **Security:**
   - Add authentication/authorization
   - Use HTTPS with SSL certificates
   - Implement rate limiting
   - Sanitize file uploads

2. **Performance:**
   - Use production ASGI server (e.g., Gunicorn with Uvicorn workers)
   - Implement file size limits
   - Add caching for frequently processed files
   - Consider using a message queue for batch processing

3. **Monitoring:**
   - Add logging middleware
   - Implement health checks
   - Use application performance monitoring (APM)

### Cloud Deployment

#### AWS (ECS/EKS)

```bash
# Build and push to ECR
aws ecr create-repository --repository-name ocr-webapp
docker tag ocr-webapp:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ocr-webapp:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ocr-webapp:latest

# Deploy using ECS or EKS
```

#### Google Cloud (Cloud Run)

```bash
gcloud builds submit --tag gcr.io/<project-id>/ocr-webapp
gcloud run deploy ocr-webapp --image gcr.io/<project-id>/ocr-webapp --port 7346
```

#### Azure (Container Instances)

```bash
az acr build --registry <registry-name> --image ocr-webapp:latest .
az container create --resource-group <rg> --name ocr-app --image <registry-name>.azurecr.io/ocr-webapp:latest --ports 7346
```

## Troubleshooting

### Common Issues

1. **Tesseract not found:**
   ```
   Error: TesseractNotFoundError
   ```
   **Solution:** Ensure Tesseract is installed and in PATH, or set `TESSERACT_PATH` environment variable.

2. **PDF processing fails:**
   ```
   Error: Poppler not installed
   ```
   **Solution:** Install `poppler-utils` system package.

3. **Memory issues with large PDFs:**
   **Solution:** Implement chunked processing or increase Docker memory limits.

4. **Language not supported:**
   ```
   Error: Language 'xx' not found
   ```
   **Solution:** Install the required Tesseract language pack.

### Logs

- **Docker logs:** `docker logs ocr-app`
- **Application logs:** Check console output or implement file logging

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add type hints where possible
- Write tests for new functionality
- Update documentation for API changes
- Keep the Docker image lightweight

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - The OCR engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [PDF2Image](https://github.com/Belval/pdf2image) - PDF to image conversion
- [Pillow](https://python-pillow.org/) - Image processing library

## Contact

- **Author**: eijisa2
- **Project Link**: [https://github.com/eijisa2/ocr-webapp](https://github.com/eijisa2/ocr-webapp)

---

**Note**: This application is designed for educational and development purposes. For production use, consider adding security measures, error handling, and scalability features.

*Last Updated: April 2026*
