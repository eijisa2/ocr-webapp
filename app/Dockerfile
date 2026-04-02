FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur tesseract-ocr-rus tesseract-ocr-eng tesseract-ocr-spa \
    libtesseract-dev poppler-utils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY ocr_utils.py .
COPY static/ ./static/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7346

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7346"]
