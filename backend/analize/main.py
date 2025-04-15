"""
This is the main file for the backend of the Best Beach project.
It contains the FastAPI application and the main functions for handling requests.
"""
from datetime import datetime, timezone, timedelta
import json
import copy
import pandas as pd
import numpy.random as rnd
from sklearn import linear_model
import pymongo
import conditions
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import model
from utils import get_beaches, change_time_zone



def rate_for_current(today: pd.DataFrame, beach: str)-> float:
    """
    Returns the foreseen "Rating" for certain conditions, in a certain beach, in a given dataframe
    :param today: list of conditions [Wind Sp, Wind Dir, Swell Hgt, Swell Dir, Swell Prd]
    :param beach: name of the beach
    :return: the foreseen rating
    """
    try:
        return model.predict(today, beach)
    except FileNotFoundError as exc:
        print(exc)
        raise SystemError("Model not found. Please train the model first.") from exc



def best_list(conditions: pd.DataFrame) -> dict[str, float]:
    """
    Returns sorted list of beaches and their rating
    :param conditions: dataframe of conditions containing the relevant data
    :return: dictionary of beaches and their rating
    """
    beach_names = get_beaches()
    beach_conditions = {}
    # conditions.insert(0, conditions.pop(0)*wind_dir(conditions.pop(0)))
    if len(beach_names) == 0:
        print("No beaches found")
        raise DataError("No beaches found")
    
    for beach in beach_names:
        x = rate_for_current(conditions, beach)
        print("For", beach,'-', x)
        beach_conditions[beach] = x
    return beach_conditions



# assign dataframe from MongoDB
def grand_mongo():
    global grand
    try:
        client = pymongo.MongoClient("mongodb+srv://"+loadKeys()['user']+":"+loadKeys()["password"]+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        db = client["Reviews"]
        collection = db["Sharon Beaches"]
    except:
        raise SystemError("Trouble connecting to server")
    jdict = {}
    docs = collection.find({})
    for doc in docs:
        jdict.update(doc)
    grand = pd.DataFrame(jdict)


# assign dataframe from review MongoDB
def grand_reviews():
    global grand
    try:
        client = pymongo.MongoClient("mongodb+srv://"+loadKeys()['user']+":"+loadKeys()["password"]+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        db = client["Reviews"]
        collection = db["From Web"]
    except:
        raise SystemError("Trouble connecting to server")
    jdict = []
    docs = collection.find({})
    for doc in docs:
        jdict.append(doc)
    grand = pd.DataFrame(jdict)


# creates a json file to use as the data source (fictive)
def update_json():
    grand = make_random_table(100)
    grand.to_json(r'~/Documents/Code/BestBeach/backend/analize/keys and data/GreatBigData.json')
    print("Done")


# assign dataframe from local json file (for testing)
def grand_json():
    global grand
    grand = pd.read_json('/home/dori/Documents/Code/BestBeach/backend/analize/keys and data/GreatBigData.json')


def loadKeys():
    f = open("/home/dori/Documents/Code/keysForMongo.json")
    data = json.load(f)
    return(data)


if __name__=="__main__":
    app = FastAPI()
    pd.set_option('display.max_rows', None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# returns calculated list of beaches for a given date-time string - formatted YYYY-MM-DD%20HH:mm
@app.get("/numcrunch/{check_for}")
def sendlist(check_for = datetime.now(timezone.utc)):
    grand_mongo()
    if check_for == "NOW": check_for = datetime.now(timezone.utc)
    elif type(check_for) == str: check_for = change_time_zone(check_for)
    this_day = conditions.day_list(check_for)
    return JSONResponse(content={"conditions": {
        "windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]}, "beachList": best_list(this_day)})


# returns conditions for a given date-time string - formatted YYYY-MM-DD%20HH:mm
@app.get("/conditions/{check_for}")
def cond_time(check_for = datetime.now(timezone.utc)):
    grand_mongo()
    if check_for == "NOW": check_for = datetime.now(timezone.utc)
    elif type(check_for) == str: check_for = change_time_zone(check_for)
    this_day = conditions.day_list(check_for)
    return JSONResponse(content={"windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]})


# adds a review to the database - time formatted YYYY-MM-DD%20HH:mm
@app.get("/addrev/datetime={dateTime}&beach={beach}&rate={rate}")
def new_review(dateTime, beach, rate):
    try:
        client = pymongo.MongoClient("mongodb+srv://"+loadKeys()['user']+":"+loadKeys()["password"]+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        db = client["Reviews"]
        collection = db["From Web"]
    except:
        return JSONResponse(content={"Response":"Error connecting to server"})
    try: row = conditions.day_list(makeIsrTime(dateTime))
    except: return JSONResponse(content={"Response":"Error handling time"})
    day_dic = {
        "Beach": beach,
        "Tide":row[5],
        "Wind Sp": row[0],
        "Wind Dir": row[1],
        "Wind Qual": wind_dir(row[1])*row[0],
        "Swell Hgt": row[2],
        "Swell Dir": row[3],
        "Swell Prd": row[4],
        "Rating": rate}
    collection.insert_one(day_dic)
    return JSONResponse(content={"Response":"Successfuly uploaded"})


#returns the beaches currently in the database
@app.get("/which_beaches")
def beaches():
    grand_mongo()
    return JSONResponse(content={"Beaches":get_beaches(grand)})


class DataError(Exception):
    """
    Custom exception for data errors
    """
    pass