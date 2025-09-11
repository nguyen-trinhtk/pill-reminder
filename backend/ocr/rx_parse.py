import requests
import re
from typing import List, Dict, Optional, Any

def is_med(name: str) -> bool:
    try:
        resp = requests.get(
            "https://rxnav.nlm.nih.gov/REST/rxcui.json", params={"name": name}, timeout=5)
        resp.raise_for_status()
        rxnorm_ids = resp.json().get("idGroup", {}).get("rxnormId", [])
        for rxcui in rxnorm_ids:
            prop_resp = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json", timeout=5)
            prop_resp.raise_for_status()
            drug_name = prop_resp.json().get("properties", {}).get("name", "")
            if drug_name.lower() == name.lower():
                return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def get_med(prescription: str):
    for word in prescription.split():
        if is_med(word):
            return word
    return None

standard_times = {
    "morning": "0800",
    "noon": "1200",
    "afternoon": "1400",
    "evening": "1800",
    "night": "2100",
    "bedtime": "2100"
}

freq_map = {
    r"\bonce daily\b|\bdaily\b|\bone time a day\b": ["0800"],
    r"\btwice daily\b|\btwo times\b|\bbid\b": ["0800", "1800"],
    r"\bthree times\b|\bthrice\b|\btid\b": ["0800", "1400", "1800"],
    r"\bfour times\b|\bqid\b": ["0800", "1200", "1400", "1800"]
}

compiled_standard_times = {key: re.compile(rf"\b{key}\b") for key in standard_times}
compiled_freq_map = {pat: re.compile(pat) for pat in freq_map}
every_hours_regex = re.compile(r"every\s*(\d+)\s*hours?")

def get_schedule(prescription: str) -> List[Dict[str, int]]:
    
    prescription = prescription.lower()
    schedule = []

    numbers = [(m.start(), int(m.group())) for m in re.finditer(r"\b\d+\b", prescription)]

    explicit_times_found = False
    for key, regex in compiled_standard_times.items():
        for match in regex.finditer(prescription):
            explicit_times_found = True
            pos = match.start()
            qty = 1
            for n_pos, n_val in reversed(numbers):
                if n_pos < pos:
                    qty = n_val
                    break
            schedule.append({"quantity": qty, "time": standard_times[key]})

    if not explicit_times_found:
        for pat, regex in compiled_freq_map.items():
            for freq_match in regex.finditer(prescription):
                pos = freq_match.start()
                qty = 1
                for n_pos, n_val in reversed(numbers):
                    if n_pos < pos:
                        qty = n_val
                        break
                for t in freq_map[pat]:
                    schedule.append({"quantity": qty, "time": t})

    for every_match in every_hours_regex.finditer(prescription):
        interval = int(every_match.group(1))
        times = [f"{h:02d}00" for h in range(8, 24, interval)]
        pos = every_match.start()
        qty = 1
        for n_pos, n_val in reversed(numbers):
            if n_pos < pos:
                qty = n_val
                break
        for t in times:
            schedule.append({"quantity": qty, "time": t})

    if not schedule:
        qty = int(numbers[-1][1]) if numbers else 1
        schedule.append({"quantity": qty, "time": "0800"})

    seen = set()
    deduped_schedule = []
    for entry in schedule:
        key = (entry["quantity"], entry["time"])
        if key not in seen:
            deduped_schedule.append(entry)
            seen.add(key)

    return deduped_schedule

def get_dosage(prescription: str) -> Dict[str, Optional[str]]:
    prescription = prescription.lower()
    
    result = {
        "dosage": None,
        "unit": None,
        "form": None
    }

    dose_match = re.search(r"(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|units|iu)\b", prescription)
    if dose_match:
        result["dosage"] = float(dose_match.group(1)) if '.' in dose_match.group(1) else int(dose_match.group(1))
        result["unit"] = dose_match.group(2)

    form_match = re.search(r"\b(tablet|capsule|pill|pills|tbsp|teaspoon|drop|patch|syrup|injection)\b", prescription)
    if form_match:
        result["form"] = form_match.group(1)

    combined_match = re.search(r"(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|units|iu)?\s*(tablet|capsule|pill|pills|tbsp|teaspoon|drop|patch|syrup|injection)?", prescription)
    if combined_match:
        if not result["dosage"] and combined_match.group(1):
            result["dosage"] = float(combined_match.group(1)) if '.' in combined_match.group(1) else int(combined_match.group(1))
        if not result["unit"] and combined_match.group(2):
            result["unit"] = combined_match.group(2)
        if not result["form"] and combined_match.group(3):
            result["form"] = combined_match.group(3)
    return result

def parse_rx(prescription: str) -> Dict[str, Any]:
    result = {
        "medication_name": None,
        "dosage": None,
        "dosage_unit": None,
        "form": None,
        "schedule": []
    }

    # Detect medication
    med = get_med(prescription)
    if med:
        result["medication_name"] = med

    # Extract dosage/unit/form
    dosage_info = get_dosage(prescription)
    if dosage_info:
        result["dosage"] = dosage_info.get("dosage")
        result["dosage_unit"] = dosage_info.get("unit")
        result["form"] = dosage_info.get("form")

    # Extract schedule
    schedule = get_schedule(prescription)
    if schedule:
        result["schedule"] = schedule

    return result

# import time
# def timed_parse(prescription: str) -> Dict[str, Any]:
#     start = time.perf_counter()
#     result = parse_rx(prescription)
#     end = time.perf_counter()
#     elapsed = end - start
#     print(f"Runtime: {elapsed:.4f} seconds")
#     return result


# rx = "Take 1 tablet of amoxicillin 500 mg twice daily in the morning and evening"
# parsed = timed_parse(rx)
# print(parsed)


