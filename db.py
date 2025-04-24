from pymongo import MongoClient
from logger import logger

client = MongoClient("mongodb://admin:secret@mongodb:27017/")
db = client['flask_mongo_app']
users_collection = db['users']

def add_user(name):
    logger.info(f"Inserting user: {name}")
    result = users_collection.insert_one({"name": name})
    logger.info(f"Inserted user ID: {result.inserted_id}")
    return str(result.inserted_id)

def get_all_users():
    logger.info("Fetching all users")
    users = list(users_collection.find({}, {"_id": 0}))
    logger.info(f"Fetched users: {users}")
    return users
