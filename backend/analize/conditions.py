import json
import requests
from datetime import datetime, timezone
import pandas as pd
import numpy


# gets the marine data from the StormGlass.io API
def pull_data(timed = timezone.now(timezone.utc)):
    response = requests.get(
    'https://api.stormglass.io/v2/weather/point',
    params={
        'lat': 32.1761,
        'lng': 34.7984,
        'params': ','.join(['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod']),  # "Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide"
        'start': timed,
        'end':  timed
    },
    headers={
        'Authorization': 'ca2bd50e-a14a-11ed-a138-0242ac130002-ca2bd572-a14a-11ed-a138-0242ac130002'
    }
    )
    return response.json()


# makes a dictionary of the desired sea conditions
def sea_dict(timed = datetime.now(timezone.utc)):
    x = {'hours': 
    [{
        'swellDirection': {'dwd': 271.02, 'icon': 268.68, 'noaa': 283.05, 'sg': 268.68}, 
        'swellHeight': {'dwd': 1.98, 'icon': 1.83, 'noaa': 0.35, 'sg': 1.83}, 
        'swellPeriod': {'dwd': 7.11, 'icon': 7.51, 'noaa': 7.64, 'sg': 7.51}, 
        'time': '2023-01-31T10:00:00+00:00', 
        'windDirection': {'icon': 274.46, 'noaa': 279.5, 'sg': 274.46}, 
        'windSpeed': {'icon': 8.51, 'noaa': 8.3, 'sg': 8.51}
    }], 
    'meta': 
    {
        'cost': 1, 'dailyQuota': 10, 'end': '2023-01-31 10:20', 'lat': 32.1761, 'lng': 34.7984, 
        'params': ['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod'], 
        'requestCount': 10, 'start': '2023-01-31 10:00'
    }}
    df = pd.DataFrame(x["hours"][0])   # REMEMBER TO SWITCH THESE^
    # df = pd.DataFrame(pull_data()["hours"][0])
    df.to_json(r'~/Documents/Code/BestBeach/backend/analize/sea_data.json')
    print(df)
    mean_val = {}
    columns = list(df)
    for col in columns:
        if col == "time":
            continue
        mean_val[col] = df[col].median()
    print(mean_val)


# gets the trinary tidal situation
def get_tide(timed = datetime.now(timezone.utc)):
    return 1


# returns "Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide" for chosen time
def day_list(timed = datetime.now(timezone.utc)):
    templ = sea_dict(timed)
    the_list = [templ["windSpeed"], templ["windDirection"], templ["swellHeight"], templ["swellDirection"], templ["swellPeriod"], get_tide(timed)]
    return the_list
