from pymongo.mongo_client import MongoClient
from bson import ObjectId, errors as bson_errors
import datetime
USERS_COLLECTION = "users"
from app.db.db_client import serialize_doc

def create_user(
    client: MongoClient,
    name: str,
    dob: datetime.datetime,
    email: str
) -> str:
    if not name or not email or not dob:
        raise ValueError("Name, email, and dob are required.")
    user = {
        'name': name,
        'dob': dob,
        'email': email,
        'created_at': datetime.datetime.now(tz=datetime.timezone.utc),
        'updated_at': datetime.datetime.now(tz=datetime.timezone.utc),
    }
    try:
        udb = client.PillReminder[USERS_COLLECTION]
        result = udb.insert_one(user)
        return str(result.inserted_id)
    except Exception as e:
        raise RuntimeError(f"Failed to create user: {e}")

def read_user(client: MongoClient, user_id: str) -> dict:
    try:
        udb = client.PillReminder[USERS_COLLECTION]
        try:
            obj_id = ObjectId(user_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid user_id format.")
        user = udb.find_one({"_id": obj_id})
        return serialize_doc(user)
    except Exception as e:
        raise RuntimeError(f"Failed to read user: {e}")
    
def update_user(
    client: MongoClient,
    user_id: str,
    name: str = None,
    dob: datetime.datetime = None,
    email: str = None
) -> bool:
    if not user_id:
        raise ValueError("User ID is required.")
    
    update_fields = {}
    if name:
        update_fields['name'] = name
    if dob:
        update_fields['dob'] = dob
    if email:
        update_fields['email'] = email
    
    if not update_fields:
        raise ValueError("No fields to update.")
    
    update_fields['updated_at'] = datetime.datetime.now(tz=datetime.timezone.utc)
    
    try:
        udb = client.PillReminder[USERS_COLLECTION]
        try:
            obj_id = ObjectId(user_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid user_id format.")
        result = udb.update_one({"_id": obj_id}, {"$set": update_fields})
        if result.matched_count == 0:
            raise ValueError("User not found.")
        return result.modified_count > 0
    except Exception as e:
        raise RuntimeError(f"Failed to update user: {e}")

def delete_user(client: MongoClient, user_id: str) -> bool:
    if not user_id:
        raise ValueError("User ID is required.")
    try:
        udb = client.PillReminder[USERS_COLLECTION]
        try:
            obj_id = ObjectId(user_id)
        except bson_errors.InvalidId:
            raise ValueError("Invalid user_id format.")
        result = udb.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise ValueError("User not found.")
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to delete user: {e}")