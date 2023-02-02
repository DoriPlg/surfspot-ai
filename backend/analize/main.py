import pandas as pd
import numpy.random as rnd
from sklearn import linear_model
import copy
import pymongo
from fastapi import FastAPI
import conditions
from datetime import datetime, timezone, timedelta


app = FastAPI()
pd.set_option('display.max_columns', None)


beach_names = ["Marina main", "Gazibo", "9Beach", "Sidni Ali"]


# returns number representing wind direction in relation to shore
# it is possible to add finer tuning!
def wind_dir(deg):
    while deg > 360 or deg < 0:
        if deg > 360:
            deg -= 360
        if deg < 0:
            deg += 360
    if 325 >= deg >= 245:
        return 2  # onshore
    elif 140 >= deg >= 70:
        return 1  # offshore
    else:
        if 20 <= deg <= 190: return 3  # side-offshore
        return 4  # side-onshore


# creates random data table, to work with. NO CORRELATION TO REALITY
def make_table(size=300):
    beach = []
    wind_q = []
    for i in range(size):
        beach.append(beach_names[rnd.randint(0, len(beach_names))])
    tide = rnd.randint(-1, 3, size)
    for i in range(size):
        if tide[i] == 1: tide[i] = 0
        if tide[i] == 2: tide[i] = 1
    actual = rnd.normal(5, 2, size)
    for i in range(size):
        actual[i] = round(actual[i], 0)
        if actual[i] > 7:
            actual[i] = 7
        if actual[i] < 1:
            actual[i] = 1
    wind_s = rnd.normal(12, 4.3, size)
    for i in range(size): wind_s[i] = round(wind_s[i], 1)
    wind_d = rnd.normal(280, 130, size)
    for i in range(size): wind_d[i] = round(wind_d[i], 0)
    for i in range(size):
        wind_q.append(wind_dir(wind_d[i])*wind_s[i])
    swell_h = rnd.normal(1.3, 0.4, size)
    for i in range(size): swell_h[i] = round(swell_h[i], 2)
    swell_d = rnd.normal(280, 10, size)
    for i in range(size):
        swell_d[i] = round(swell_d[i], 0)
        if swell_d[i] > 360:
            swell_d[i] = 360
        if swell_d[i] < 200:
            swell_d[i] = 200
    swell_p = rnd.normal(8.0, 1.5, size)
    for i in range(size): swell_p[i] = round(swell_p[i], 0)
    tab = {
        "Beach": beach,
        "Tide": tide,
        "Wind Sp": wind_s,
        "Wind Dir": wind_d,
        "Wind Qual": wind_q,
        "Swell Hgt": swell_h,
        "Swell Dir": swell_d,
        "Swell Prd": swell_p,
        "Actual": actual
    }
    return pd.DataFrame(tab)


# returns the foreseen "actual" rating for certain conditions, in a certain beach, in a given dataframe
def rate_for_current(today: list, beach: str, main_data: pd.DataFrame):
    df = copy.copy(main_data)
    for x in df.index:
        if df.loc[x, "Tide"] != today[-1]:
            df.drop(x, inplace=True)
    # print(df)
    for x in df.index:
        if df.loc[x, "Beach"] != beach:
            df.drop(x, inplace=True)
    X = df[["Wind Qual", "Swell Hgt", "Swell Dir", "Swell Prd"]]
    y = df["Actual"]
    regress = linear_model.LinearRegression()
    regress.fit(X.values, y)
    today = [today[0:-1:]]
    # print(df)
    return regress.predict(today)


# returns sorted list of beaches and their rating
def best_list(conditions: list):
    cond_list = []
    conditions.insert(0, conditions.pop(0)*wind_dir(conditions.pop(0)))
    global beach_names
    for i in beach_names:
        x = rate_for_current(conditions, i, grand)[0]
        # print(x)
        a = 0
        try:
            while x < cond_list[a][1]:
                a += 1
            cond_list.insert(a, [i, x])
        except:
            cond_list.append([i, x])
    return cond_list


# creates a json file to use as the data source (fictive)
def update_json():
    grand = make_table(100)
    grand.to_json(r'~/Documents/Code/BestBeach/backend/analize/keys and data/GreatBigData.json')
    print("Done")


cl_name = "DoriP"
client = pymongo.MongoClient("mongodb+srv://"+cl_name+":"+input("What's your password, "+cl_name+"? ")+"@cluster0.loj5c73.mongodb.net/?retryWrites=true&w=majority")
db = client["my_db"]
collection = db['wave_days']
jdict = {}
docs = collection.find({})
for doc in docs:
    jdict.update(doc)
grand = pd.DataFrame(jdict)
pd.set_option('display.max_rows', None)

@app.get("/numcrunch")
def sendlist(check_for = datetime.now(timezone.utc)):
    this_day = conditions.day_list(check_for)
    result = {"conditions": {"windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]}, "beachList": best_list(this_day)}
    return result


@app.get("/conditions")
def cond_time(check_for = datetime.now(timezone.utc)):
    this_day = conditions.day_list(check_for)
    return {"windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]}