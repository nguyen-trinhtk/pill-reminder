from pymongo.mongo_client import MongoClient
from bson import ObjectId, errors as bson_errors
import datetime

USERS_COLLECTION = "users"
PRESCRIPTIONS_COLLECTION = "prescriptions"

def serialize_doc(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    for k, v in doc.items():
        if isinstance(v, datetime.datetime):
            doc[k] = v.isoformat()
    return doc

def create_prescription(
    client: MongoClient,
    user_id: str,
    medication: str,
    dosage: str,
    instructions: str,
    frequency: int,
    times: list
) -> str:
    if not user_id:
        raise ValueError("User ID is required.")
    if not medication or not dosage or not instructions or frequency is None or not times:
        raise ValueError("All prescription fields are required.")
    try:
        udb = client.PillReminder[USERS_COLLECTION]
        pdb = client.PillReminder[PRESCRIPTIONS_COLLECTION]
        try:
            obj_id = ObjectId(user_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid user_id format.")
        user = udb.find_one({"_id": obj_id})
        if not user:
            raise ValueError("User does not exist.")
    except Exception as e:
        raise RuntimeError(f"Failed to validate user: {e}")
    times = [t.strftime("%H:%M") if isinstance(t, datetime.time) else str(t) for t in times]
    prescription = {
        'user_id': str(user_id),
        'medication': medication,
        'dosage': dosage,
        'instructions': instructions,
        'frequency': frequency,
        'time': times,
        'created_at': datetime.datetime.now(tz=datetime.timezone.utc),
    }
    try:
        result = pdb.insert_one(prescription)
        return str(result.inserted_id)
    except Exception as e:
        raise RuntimeError(f"Failed to create prescription: {e}")

def read_prescriptions(client: MongoClient, user_id: str) -> list:
    if not user_id:
        raise ValueError("User ID is required.")
    try:
        pdb = client.PillReminder[PRESCRIPTIONS_COLLECTION]
        prescriptions = [serialize_doc(p) for p in pdb.find({"user_id": user_id})]
        return prescriptions
    except Exception as e:
        raise RuntimeError(f"Failed to read prescriptions: {e}")
    
def update_prescription(
    client: MongoClient,
    presc_id: str,
    medication: str = None,
    dosage: str = None,
    instructions: str = None,
    frequency: int = None,
    times: list = None
) -> bool:
    if not presc_id:
        raise ValueError("Prescription ID is required.")
    update_fields = {}
    if medication:
        update_fields['medication'] = medication
    if dosage:
        update_fields['dosage'] = dosage
    if instructions:
        update_fields['instructions'] = instructions
    if frequency is not None:
        update_fields['frequency'] = frequency
    if times is not None:
        times = [t.strftime("%H:%M") if isinstance(t, datetime.time) else str(t) for t in times]
        update_fields['time'] = times
    if not update_fields:
        raise ValueError("No fields to update.")
    try:
        pdb = client.PillReminder[PRESCRIPTIONS_COLLECTION]
        try:
            obj_id = ObjectId(presc_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid prescription_id format.")
        result = pdb.update_one({"_id": obj_id}, {"$set": update_fields})
        if result.matched_count == 0:
            raise ValueError("Prescription not found.")
        return result.modified_count > 0
    except Exception as e:
        raise RuntimeError(f"Failed to update prescription: {e}")

def delete_prescription(client: MongoClient, presc_id: str) -> bool:
    if not presc_id:
        raise ValueError("Prescription ID is required.")
    try:
        pdb = client.PillReminder[PRESCRIPTIONS_COLLECTION]
        try:
            obj_id = ObjectId(presc_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid prescription_id format.")
        result = pdb.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise ValueError("Prescription not found.")
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to delete prescription: {e}")
