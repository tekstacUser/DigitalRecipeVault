from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
db = client["test_db"]

users_collection = db["users"]
recipes_collection = db["recipes"]
