import pymongo

client = pymongo.MongoClient("mongodb+srv://DoriP:"+input("What's your password, DoriP?")+"@cluster0.loj5c73.mongodb.net/?retryWrites=true&w=majority")
db = client["my_db"]
collection = db['wave_days']

docs = collection.find({})
for doc in docs:
    print(doc)

