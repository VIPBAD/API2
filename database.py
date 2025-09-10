from pymongo import MongoClient
from bson.objectid import ObjectId

class Database:
    def __init__(self, uri="mongodb+srv://BADMUNDA:BADMYDAD@badhacker.i5nw9na.mongodb.net/"):
        self.client = MongoClient(uri)
        self.db = self.client["telegram_music"]
        self.collection = self.db["user_history"]

    def save_history(self, user_id, title, duration):
        history = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "timestamp": datetime.datetime.utcnow()
        }
        result = self.collection.insert_one(history)
        return str(result.inserted_id)

    def get_recent_history(self, user_id, limit=3):
        history = self.collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        return list(history)

    def close(self):
        self.client.close()
