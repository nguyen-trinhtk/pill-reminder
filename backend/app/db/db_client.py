from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os


USERS_COLLECTION = "users"
PRESCRIPTIONS_COLLECTION = "prescriptions"

load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PW = os.getenv('MONGO_PW')
if not MONGO_USER or not MONGO_PW:
    raise EnvironmentError("MONGO_USER or MONGO_PW not set in environment variables. Check your .env file.")
MONGO_URI = f"mongodb+srv://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PW)}@pillreminder.movphs7.mongodb.net/?retryWrites=true&w=majority&appName=PillReminder"

def get_client() -> MongoClient:
    return MongoClient(MONGO_URI, server_api=ServerApi('1'))

def close_client(client: MongoClient) -> None:
    client.close()