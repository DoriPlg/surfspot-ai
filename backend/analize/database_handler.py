"""
This module handles the connection to the MongoDB database.
"""

import json
import pymongo



def load_keys()->dict[str, str]:
    """
    Loads the keys for MongoDB from a json file
    :return: dictionary with the keys
    :raises FileNotFoundError: if the mongoDB keys are not in place
    """
    f = open("../keysForMongo.json", "r", encoding="utf-8")
    if f is None:
        raise FileNotFoundError("File not found, please make sure the file located in"\
                                        "the proper directory\n../keysForMongo.json")
    keys = json.load(f)
    f.close()
    return keys

def connect_to_mongo() -> pymongo.MongoClient:
    """
    Connects to the MongoDB database
    :return: MongoDB client
    :raises FileNotFoundError: if the mongoDB keys are not in place
    """
    key = load_keys()

    try:
        client: pymongo.MongoClient = pymongo.MongoClient(
                f"mongodb+srv://{key['user']}:{key["password"]}@\
                cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        return client
    except pymongo.errors.ConnectionFailure as e:
        raise ConnectionError("Trouble connecting to server") from e
