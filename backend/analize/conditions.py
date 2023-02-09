import requests
from datetime import datetime, timezone, timedelta
import pandas as pd

key = "ca2bd50e-a14a-11ed-a138-0242ac130002-ca2bd572-a14a-11ed-a138-0242ac130002"

# gets the marine data from the StormGlass.io API
def pull_data(timed = datetime.now(timezone.utc)):
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
        'Authorization': key
    }
    )
    res = response.json()
    f = open("/home/dori/Documents/Code/BestBeach/backend/analize/keys and data/pulls.txt", "a")
    f.write(str(res))
    f.close()
    return res


# makes a dictionary of the desired sea conditions
def sea_dict(timed = datetime.now(timezone.utc)):
    """
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
    """
    df = pd.DataFrame(pull_data(timed)["hours"][0])
    mean_val = {}
    columns = list(df)
    for col in columns:
        if col == "time":
            continue
        mean_val[col] = df[col].median()
    return mean_val


# gets the trinary tidal situation
def get_tide(timed = datetime.now(timezone.utc)):
    #"""
    start = timed - timedelta(0, 0, 0, 0, 12.5, 6, 0)
    stop = timed +  timedelta(0, 0, 0, 0, 12.5, 6, 0)
    response = requests.get(
    'https://api.stormglass.io/v2/tide/extremes/point',
    params={
        'lat': 32.1761,
        'lng': 34.7984,
        'start': start,  # Convert to UTC timestamp
        'end': stop,  # Convert to UTC timestam
    },
    headers={
        'Authorization': key
    }
    )
    d_tide = response.json()
    f = open("/home/dori/Documents/Code/BestBeach/backend/analize/keys and data/pulls.txt", "a")
    f.write(str(d_tide))
    f.close()
    #"""
    # d_tide = [{'height': 0.012778267802382953, 'time': '2023-02-07T06:04:00+00:00', 'type': 'high'}, {'height': -0.0261013218364069, 'time': '2023-02-07T10:43:00+00:00', 'type': 'low'}, {'height': 0.08379443397049985, 'time': '2023-02-07T17:25:00+00:00', 'type': 'high'}]  
    min_delta = 7*3600
    ref = None
    for i in d_tide:
        duration = datetime.strptime(i["time"],'%Y-%m-%dT%H:%M:%S%z')-timed
        delta = abs(duration.total_seconds())
        if delta<min_delta:
            if i["type"] == 'high': dir = 1
            elif i["type"] == 'low': dir = -1
            min_delta = delta
    if 90 < abs(divmod(min_delta, 60)[0]) < 282:
        return 0
    return dir


# returns "Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide" for chosen time
def day_list(timed = datetime.now(timezone.utc)):
    templ = sea_dict(timed)
    the_list = [templ["windSpeed"], templ["windDirection"], templ["swellHeight"], templ["swellDirection"], templ["swellPeriod"], get_tide(timed)]
    return the_list

