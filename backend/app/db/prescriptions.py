from pymongo.mongo_client import MongoClient
from bson import ObjectId, errors as bson_errors
import datetime
from app.db.db_client import serialize_doc

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
    medication_name: str,
    dosage: float,
    dosage_unit: str,
    form: str,
    schedule: list  # list of dicts: [{'quantity': int, 'time': str}]
) -> str:
    if not user_id:
        raise ValueError("User ID is required.")
    if not medication_name or dosage is None or not dosage_unit or not form or not schedule:
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
    prescription = {
        'user_id': str(user_id),
        'medication_name': medication_name,
        'dosage': dosage,
        'dosage_unit': dosage_unit,
        'form': form,
        'schedule': schedule,
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
    medication_name: str = None,
    dosage: float = None,
    dosage_unit: str = None,
    form: str = None,
    schedule: list = None
) -> bool:
    if not presc_id:
        raise ValueError("Prescription ID is required.")
    update_fields = {}
    if medication_name:
        update_fields['medication_name'] = medication_name
    if dosage is not None:
        update_fields['dosage'] = dosage
    if dosage_unit:
        update_fields['dosage_unit'] = dosage_unit
    if form:
        update_fields['form'] = form
    if schedule is not None:
        update_fields['schedule'] = schedule
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
