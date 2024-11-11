from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


class MongoDBConnection:
    def __init__(
        self,
        url=os.environ.get("MONGODB_URL"),
        db_name=os.environ.get("MONGODB_NAME"),
    ):
        self.url = url
        self.db_name = db_name
        self.client = None
        self.db = None

    def __enter__(self):
        self.client = MongoClient(self.url)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_value, trace):
        if self.client:
            self.client.close()
