from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from datetime import datetime
from io import BytesIO
from PIL import Image

from ocr_utils import (
    process_image_with_tesseract,
    is_image_file,
    is_pdf_file,
    pdf_to_images_in_memory
)

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.post("/api/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    language: str = Form("auto")
):
    SUPPORTED_LANGUAGES = {
        "auto": "eng",
        "en": "eng",
        "tr": "tur",
        "ru": "rus",
        "es": "spa",
    }
    lang_code = SUPPORTED_LANGUAGES.get(language, "eng")
    ocr_results = []

    for file in files:
        filename = file.filename
        uploaded_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        try:
            content = await file.read()
            if is_image_file(filename):
                img = Image.open(BytesIO(content))
                text = process_image_with_tesseract(img, lang_code)
            elif is_pdf_file(filename):
                images = pdf_to_images_in_memory(content)
                text = ""
                for img in images:
                    text += process_image_with_tesseract(img, lang_code)
            else:
                text = "Unsupported file format."
        except Exception as e:
            text = f"Error: {str(e)}"

        ocr_results.append({
            "filename": filename,
            "date": uploaded_date,
            "language": language,
            "status": "done" if not text.startswith("Error:") else "error",
            "text": text
        })

    return JSONResponse(content={"results": ocr_results})

@app.get("/api/health")
def health():
    return {"status": "ok"}
