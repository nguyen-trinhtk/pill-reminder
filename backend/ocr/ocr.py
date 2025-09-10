import pytesseract
import cv2
import os
import re

STOP_WORDS = {"TAB", "TABLET", "CAP", "CAPSULE"}

time_map = {
    "morning": "08:00",
    "noon": "12:00",
    "afternoon": "16:00",
    "evening": "18:00",
    "bedtime": "22:00"
}

def preprocess_image(img_path):
    """Preprocess image for better OCR (grayscale + threshold)."""
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {img_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return bw

def clean_text(text):
    """Basic OCR cleanup: fix missing spaces and normalize."""
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def parse_rx_label(text):
    result = {
        "medication": None,
        "dosage": None,
        "dosage_unit": None,
        "instructions": None,
        "frequency": None,
        "times": []
    }

    text = clean_text(text)

    # ---- Extract medication name + dosage ----
    med_match = re.search(r"([A-Z][A-Z\s\-]+?)\s+(\d+(?:\.\d+)?)\s*(MG|ML)", text, re.IGNORECASE)
    if med_match:
        name = med_match.group(1).title().strip()
        tokens = [t for t in name.split() if t.upper() not in STOP_WORDS]
        result["medication"] = " ".join(tokens)
        result["dosage"] = med_match.group(2)
        result["dosage_unit"] = med_match.group(3).lower()

    # ---- Extract instructions ----
    instr_match = re.search(r"(TAKE[^.;\n]*)", text, re.IGNORECASE)
    if instr_match:
        instructions = instr_match.group(1)
        instructions = re.split(r"(METOPROLOL|[A-Z]{3,}\s)", instructions)[0]
        result["instructions"] = instructions.strip()
    if not result["instructions"]:
        result["instructions"] = "Take as directed"

    # ---- Frequency parsing ----
    freq = None
    times = []
    if re.search(r"ONCE DAILY|ONCE A DAY|QD", text, re.IGNORECASE):
        freq, times = 1, [time_map["morning"]]
    elif re.search(r"TWICE A DAY|BID", text, re.IGNORECASE):
        freq, times = 2, [time_map["morning"], time_map["evening"]]
    elif re.search(r"THREE TIMES A DAY|TID", text, re.IGNORECASE):
        freq, times = 3, [time_map["morning"], time_map["afternoon"], time_map["evening"]]
    elif re.search(r"FOUR TIMES A DAY|QID", text, re.IGNORECASE):
        freq, times = 4, [time_map["morning"], time_map["noon"], time_map["evening"], time_map["bedtime"]]
    elif re.search(r"EVERY (\d+) HOURS", text, re.IGNORECASE):
        hours = int(re.search(r"EVERY (\d+) HOURS", text, re.IGNORECASE).group(1))
        freq = 24 // hours
        times = [f"{(i*hours)%24:02d}:00" for i in range(freq)]

    result["frequency"] = freq
    result["times"] = times

    return result

# ---- MAIN ----
img_path = os.path.join('./img', 'test3.jpg')
try:
    processed_img = preprocess_image(img_path)
    ocr_text = pytesseract.image_to_string(processed_img)
    cleaned_text = " ".join(line.strip() for line in ocr_text.splitlines() if line.strip())
    print("OCR TEXT:", cleaned_text, "\n")
    print(parse_rx_label(cleaned_text))
except FileNotFoundError as e:
    print(e)
