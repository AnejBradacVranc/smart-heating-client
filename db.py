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
			
	def find_all(self, collection_name):
		try:
			collection = self.db[collection_name]
			documents = list(collection.find())
			return documents
		except Exception as e:
			print("Error fetching documents:", e)
			return []
			
	def find_one(self, collection_name, filter_query=None):
		try:
			collection = self.db[collection_name]
			if filter_query is None:
				result = collection.find_one()
			else:
				result = collection.find_one(filter_query)
			return result
		except Exception as e:
			print("Error finding document:", e)
			return None
			

	def update_one(self, collection_name, item, filter_query=None, upsert=False):
		try:
			collection = self.db[collection_name]
			update = {"$set": item}
			filter_query = filter_query or {}  # Use {} if no filter provided
			result = collection.find_one_and_update(
				filter_query,
				update,
				upsert=upsert,
				return_document=ReturnDocument.AFTER
			)
			if result:
				return result["_id"]
			else:
				print("No matching document found to update.")
				return None					
		except Exception as e:
			print("Error updating one document:", e)
			return None


