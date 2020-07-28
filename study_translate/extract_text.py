import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
print(pytesseract.image_to_string('./pdf_img/pdf_00.jpg'))