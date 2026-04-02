from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

def is_image_file(filename):
    ext = filename.lower().rsplit('.', 1)[-1]
    return ext in {"jpg", "jpeg", "png", "bmp", "gif", "tiff"}

def is_pdf_file(filename):
    ext = filename.lower().rsplit('.', 1)[-1]
    return ext == "pdf"

def process_image_with_tesseract(img_or_file, lang_code="eng"):
    return pytesseract.image_to_string(img_or_file, lang=lang_code)

def pdf_to_images_in_memory(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images
