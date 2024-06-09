import pytesseract
from PIL import Image

def perform_ocr(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 3')
    return text
