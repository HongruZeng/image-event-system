from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()


class DocumentDBService:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise ValueError("MONGO_URI is missing. Please check your .env file.")

        self.client = MongoClient(
            mongo_uri,
            tls=True,
            tlsAllowInvalidCertificates=True
        )

        self.db = self.client["image_event_system"]
        self.collection = self.db["annotations"]

    def save_annotation(self, image_id, annotation):
        document = {
            "image_id": image_id,
            "objects": annotation.get("objects", []),
            "source": annotation.get("source", "simulated_inference"),
            "history": ["annotation.stored"]
        }

        self.collection.update_one(
            {"image_id": image_id},
            {"$set": document},
            upsert=True
        )

        return document

    def get_annotation(self, image_id):
        return self.collection.find_one(
            {"image_id": image_id},
            {"_id": 0}
        )
