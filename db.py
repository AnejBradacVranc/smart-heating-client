from pymongo import MongoClient
class MongoDBClient: 
	def __init__(self, uri="mongodb://localhost:27017/", db_name="smartHome"):
		self.client = MongoClient(uri)
		self.db = self.client[db_name]
		
	def insert(collection_name, item):
		try:
			collection = self.db[collection_name]
			result = collection.insert_one(item)
			print("inserted document id:", result.inserted_id)
			return result.inserted_id
		except Exception as e:
			print("Error inserting document:", e)
			return None

