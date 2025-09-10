import pytesseract
import cv2
import os
import re
import requests
from difflib import get_close_matches

# Map standard times of day
time_map = {
    "morning": "08:00",
    "noon": "12:00",
    "afternoon": "16:00",
    "evening": "18:00",
    "bedtime": "22:00"
}

# ---------------- IMAGE PREPROCESSING ----------------
import cv2
import numpy as np

def adjust_gamma(image, gamma=1.2):
    """
    Adjust image gamma to brighten/darken.
    Gamma > 1: darker, Gamma < 1: brighter
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in range(256)]).astype("uint8")
    return cv2.LUT(image, table)

def preprocess_image(img_path):
    """
    Read image, enhance contrast, apply gamma correction, and binarize for OCR.
    Returns a binary image ready for Tesseract.
    """
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {img_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE (local contrast enhancement)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # Optional gamma correction to brighten slightly
    gray = adjust_gamma(gray, gamma=1.2)

    # Apply Otsu's threshold to binarize
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary


# ---------------- RXNORM CANDIDATES ----------------
def fetch_rxnorm_candidates(name):
    """Query RxNorm getDrugs endpoint and return candidate medication names."""
    try:
        url = "https://rxnav.nlm.nih.gov/REST/drugs.json"
        resp = requests.get(url, params={"name": name}, timeout=5)
        data = resp.json()
        candidates = []
        if "drugGroup" in data and "conceptGroup" in data["drugGroup"]:
            for group in data["drugGroup"]["conceptGroup"]:
                if "conceptProperties" in group:
                    for c in group["conceptProperties"]:
                        candidates.append(c.get("name"))
        return candidates
    except Exception:
        return []

# ---------------- MEDICATION NAME CLEANING ----------------
def clean_med_name_for_rxnorm(raw_name):
    """Remove OCR artifacts and form words before querying RxNorm."""
    noise_words = ["Day", "Tab", "Tablet", "Cap", "Capsule", "Oral", "Liquid", "Syrup", "Patch", "Solution"]
    pattern = r'\b(?:' + '|'.join(noise_words) + r')\b'
    cleaned = re.sub(pattern, '', raw_name, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r'[^A-Za-z0-9\s-]', '', cleaned)
    return cleaned

def correct_medication_name(raw_name):
    """
    Take raw OCR string, generate 1-3 word sequences,
    query RxNorm, and return the closest match.
    """
    cleaned_name = clean_med_name_for_rxnorm(raw_name)
    words = cleaned_name.split()
    best_match = cleaned_name
    best_score = 0

    for i in range(len(words)):
        for j in range(1, 4):
            if i + j <= len(words):
                seq = " ".join(words[i:i+j])
                rx_candidates = fetch_rxnorm_candidates(seq)
                if rx_candidates:
                    match = get_close_matches(seq, rx_candidates, n=1, cutoff=0.6)
                    if match and len(match[0]) > best_score:
                        best_match = match[0]
                        best_score = len(match[0])
    return best_match

# ---------------- PARSING FUNCTION ----------------
def parse_rx_label(text):
    result = {
        "medication": None,
        "dosage": None,
        "dosage_unit": None,
        "form": None,
        "instructions": None,
        "frequency": None,
        "times": []
    }

    # Extract form first
    form_match = re.search(r"\b(TAB|TABLET|CAP|CAPSULE|ORAL|LIQUID|SYRUP|PATCH|SOLUTION)\b", text, re.IGNORECASE)
    if form_match:
        result["form"] = form_match.group(1).lower()

    # Extract medication name + dosage
    med_match = re.search(
        r"([A-Z][a-zA-Z\-]+(?:\s+[A-Z][a-zA-Z\-]+)*)\s*(\d+(?:\.\d+)?)\s*(MG|ML)",
        text,
        re.IGNORECASE
    )
    if med_match:
        raw_med_name = med_match.group(1).title().strip()
        result["medication"] = correct_medication_name(raw_med_name)
        result["dosage"] = med_match.group(2)
        result["dosage_unit"] = med_match.group(3).lower()

    # Instructions: capture TAKE... up to first rx number, EXPIRATION, NO REFILLS, or end of string
    instr_match = re.search(r"(TAKE.*?)(?:rx\d+|EXPIRATION|NO REFILLS|$)", text, re.IGNORECASE | re.DOTALL)
    if instr_match:
        instr = instr_match.group(1).strip()
        # Clean extra symbols or noise
        instr = re.sub(r"(REFILL|ID|rx\d+|EXPIRATION|DATE|[^\w\s,-])+", "", instr, flags=re.IGNORECASE).strip()
        result["instructions"] = instr

    # Frequency detection
    freq, times = None, []
    # Existing patterns
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
    # New pattern: UP TO X TIMES DAILY
    else:
        freq_match = re.search(r"UP TO (\d+) TIMES DAILY", text, re.IGNORECASE)
        if freq_match:
            freq = int(freq_match.group(1))
            if freq == 1:
                times = [time_map["morning"]]
            elif freq == 2:
                times = [time_map["morning"], time_map["evening"]]
            elif freq == 3:
                times = [time_map["morning"], time_map["afternoon"], time_map["evening"]]
            elif freq == 4:
                times = [time_map["morning"], time_map["noon"], time_map["evening"], time_map["bedtime"]]

    result["frequency"] = freq
    result["times"] = times

    return result

# ---------------- MAIN ----------------
img_path = os.path.join('./img', 'test2.jpg')
try:
    processed_img = preprocess_image(img_path)
    ocr_text = pytesseract.image_to_string(processed_img)
    cleaned_text = " ".join(line.strip() for line in ocr_text.splitlines() if line.strip())
    parsed = parse_rx_label(cleaned_text)
    print(parsed)
except FileNotFoundError as e:
    print(e)
