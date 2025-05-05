from pymongo import MongoClient
from bson.objectid import ObjectId
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
    users = list(users_collection.find({}, {"_id": 1, "name": 1}))
    for user in users:
        user["id"] = str(user.pop("_id"))
    logger.info(f"Fetched users: {users}")
    return users

def get_user_by_id(user_id):
    logger.info(f"Fetching user by ID: {user_id}")
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 1, "name": 1})
        if user:
            user["id"] = str(user.pop("_id"))
            return user
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
    return None

def delete_user(user_id):
    logger.info(f"Deleting user by ID: {user_id}")
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            logger.info(f"Deleted user ID: {user_id}")
            return True
        else:
            logger.warning(f"User not found for deletion: {user_id}")
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
    return False
