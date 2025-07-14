import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import platform
import os

# ✅ Set correct path based on OS
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif platform.system() == "Linux":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Default Linux path (Render, Docker etc.)

def extract_text_from_file(file_path):
    extracted_text = ""

    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path)
        for image in images:
            extracted_text += pytesseract.image_to_string(image)
    else:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)

    return extracted_text
