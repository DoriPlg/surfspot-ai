import pymongo

client = pymongo.MongoClient("mongodb://localhost:27018/")
db = client["my_db"]
collection = db['bestbeaches']

docs = collection.find({})
for doc in docs:
    print(doc)

