import pandas as pd
import numpy.random as rnd
from sklearn import linear_model
import copy
import pymongo
from fastapi import FastAPI
import conditions
from datetime import datetime, timezone, timedelta


app = FastAPI()
# pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



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
def make_table(size=100):
    beach_names = ["Marina main", "Gazibo", "9Beach", "Sidni Ali"]
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
    try:
        regress = linear_model.LinearRegression()
        regress.fit(X.values, y)
        today = [today[0:-1:]]
        return regress.predict(today)[0]
    except:
        if len(df.index) < 3: return "Not enough data to calculate"
        else: return "An unknown error occurred"


# returns the names of the beaches currently in the DataFrame
def get_beaches(df: pd.DataFrame):
    beach_list = df["Beach"].tolist()
    beach_set = set()
    for i in beach_list: beach_set.add(i)
    beach_list = []
    for a in beach_set: beach_list.append(a)
    return beach_list


# returns sorted list of beaches and their rating
def best_list(conditions: list):
    beach_names = []
    cond_list = []
    conditions.insert(0, conditions.pop(0)*wind_dir(conditions.pop(0)))
    if len(beach_names) == 0: beach_names = get_beaches(grand)
    for i in beach_names:
        x = rate_for_current(conditions, i, grand)
        if type(x) == str: 
            print("For", i,'-', x)
            continue
        a = 0
        try:
            while x < cond_list[a][1]:
                a += 1
            cond_list.insert(a, [i, x])
        except:
            cond_list.append([i, x])
    return cond_list


def makeIsrTime(timeString: str):
    timeString = datetime.strptime(timeString, "%Y-%m-%d %H:%M")- timedelta(0, 0, 0, 0, 0, 2, 0)
    timeString = timeString.replace(tzinfo=timezone.utc)
    return timeString


# assign dataframe from MongoDB
def grand_mongo():
    global grand
    cl_name = "DoriP"
    client = pymongo.MongoClient("mongodb+srv://"+cl_name+":"+input("What's your password, "+cl_name+"? ")+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
    db = client["Reviews"]
    collection = db["Sharon Beaches"]
    jdict = {}
    docs = collection.find({})
    for doc in docs:
        jdict.update(doc)
    grand = pd.DataFrame(jdict)


def grand_reviews():
    global grand
    cl_name = "DoriP"
    client = pymongo.MongoClient("mongodb+srv://"+cl_name+":"+input("What's your password, "+cl_name+"? ")+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
    db = client["Reviews"]
    collection = db["From Web"]
    jdict = []
    docs = collection.find({})
    for doc in docs:
        jdict.append(doc)
    grand = pd.DataFrame(jdict)

# creates a json file to use as the data source (fictive)
def update_json():
    grand = make_table(100)
    grand.to_json(r'~/Documents/Code/BestBeach/backend/analize/keys and data/GreatBigData.json')
    print("Done")


#assign dataframe from local json file (for testing)
def grand_json():
    global grand
    grand = pd.read_json('/home/dori/Documents/Code/BestBeach/backend/analize/keys and data/GreatBigData.json')


# returns calculated list of beaches for a given date-time string - formatted YYYY-MM-DD%20HH:mm
@app.get("/numcrunch/#/{check_for}")
def sendlist(check_for = datetime.now(timezone.utc)):
    grand_mongo()
    if check_for == "NOW": check_for = datetime.now(timezone.utc)
    elif type(check_for) == str: check_for = makeIsrTime(check_for)
    this_day = conditions.day_list(check_for)
    result = {"conditions": {"windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]}, "beachList": best_list(this_day)}
    return result


# returns conditions for a given date-time string - formatted YYYY-MM-DD%20HH:mm
@app.get("/conditions/#/{check_for}")
def cond_time(check_for = datetime.now(timezone.utc)):
    grand_mongo()
    if check_for == "NOW": check_for = datetime.now(timezone.utc)
    elif type(check_for) == str: check_for = makeIsrTime(check_for)
    this_day = conditions.day_list(check_for)
    return {"windSpeed":this_day[0], "windDirection":this_day[1], "swellHeight":this_day[2], "swellDirection":this_day[3], "swellPeriod":this_day[4], "tide":this_day[5]}


# adds a review to the database - time formatted YYYY-MM-DD%20HH:mm
@app.get("/addrev/datetime={dateTime}&beach={beach}&rate={rate}")
def new_review(dateTime, beach, rate):
    try:
        cl_name = "DoriP"
        client = pymongo.MongoClient("mongodb+srv://"+cl_name+":"+input("What's your password, "+cl_name+"? ")+"@cluster0.s7lzszz.mongodb.net/?retryWrites=true&w=majority")
        db = client["Reviews"]
        collection = db["From Web"]
    except:
        return "Error connecting to server"
    try: row = conditions.day_list(makeIsrTime(dateTime))
    except: return "Error handling time"
    day_dic = {
        "Beach": beach,
        "Tide":row[5],
        "Wind Sp": row[0],
        "Wind Dir": row[1],
        "Wind Qual": wind_dir(row[1])*row[0],
        "Swell Hgt": row[2],
        "Swell Dir": row[3],
        "Swell Prd": row[4],
        "Actual": rate}
    collection.insert_one(day_dic)
    return "Successfuly uploaded"


#returns the beaches currently in the database
@app.get("/which_beaches")
def beaches():
    grand_mongo()
    return get_beaches(grand)
