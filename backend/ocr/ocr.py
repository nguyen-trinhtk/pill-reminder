import pytesseract
from textblob import TextBlob

def ocr_core(img):
    text = pytesseract.image_to_string(img)
    text = text.lower()
    text = "\n".join(line for line in text.splitlines() if line.strip())
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    corrected_text = corrected_text
    return corrected_text

