"""
This module handles the connection to the MongoDB database.
"""

import json
import pymongo



def load_keys()->dict[str, str]:
    """
    Loads the keys for MongoDB from a json file
    :return: dictionary with the keys
    """
    f = open("../keysForMongo.json", "r", encoding="utf-8")
    if f is None:
        raise SystemError("File not found")
    keys = json.load(f)
    f.close()
    return keys

def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to the MongoDB database
    :return: MongoDB client
    """
    try:
        key = load_keys()
    except FileNotFoundError as e:
        raise SystemError("File not found") from e
    try:
        client = pymongo.MongoClient(
                f"mongodb+srv://{key['user']}:{key["password"]}@\
                cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        return client
    except pymongo.errors.ConnectionFailure as e:
        raise SystemError("Trouble connecting to server") from e


