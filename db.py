from pymongo import MongoClient
from pymongo import ReturnDocument

class MongoDBClient: 
	def __init__(self, uri="mongodb://localhost:27017/", db_name="smartHome"):
		self.client = MongoClient(uri)
		self.db = self.client[db_name]
		
	def insert(self, collection_name, item):
		try:
			collection = self.db[collection_name]
			result = collection.insert_one(item)
			print("inserted document id:", result.inserted_id)
			return result.inserted_id
		except Exception as e:
			print("Error inserting document:", e)
			return None
			
	def update(self, collection_name, filter_query, item):
		try:
			collection = self.db[collection_name]		
			update={"$set": item}
			result = collection.find_one_and_update(
			filter_query,
			update,
			upsert=True,                
			return_document=ReturnDocument.AFTER)
			return result["_id"]
			print("updated document id:", result.inserted_id)
			return result.inserted_id
		except Exception as e:
			print("Error inserting document:", e)
			return None
