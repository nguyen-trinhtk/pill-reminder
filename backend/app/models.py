from flask import current_app
from datetime import datetime

def log_dispense_event(user_id: str, pill_type: str):
    db = current_app.db
    db.dispense_logs.insert_one({
        "user_id": user_id,
        "pill_type": pill_type,
        "timestamp": datetime.utcnow()
    })

def get_dispense_logs(user_id: str):
    db = current_app.db
    return list(db.dispense_logs.find({"user_id": user_id}).sort("timestamp", -1).limit(10))
