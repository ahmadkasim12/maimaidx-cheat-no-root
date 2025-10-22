from typing import Any
from pymongo import MongoClient
from pymongo.synchronous.database import Database

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "siakad"


client: MongoClient[Any] = MongoClient(MONGO_URI)
db: Database[Any] = client[DB_NAME]

print(client.list_database_names())
