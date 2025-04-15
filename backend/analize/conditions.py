"""
This module pulls data from the Stormglass API and returns a dictionary of
the desired sea conditions. It also provides functions to get the tide situation
and a list of conditions for a given time.
"""
from datetime import datetime, timezone, timedelta
import pandas as pd
import requests
from utils import read_key


DATA_PARAMS =\
    ['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod']
    # tide pulled separately
ACCESS_KEY = read_key()
PULL_PARAMS = {
        'lat': 32.1761,
        'lng': 34.7984,
        'params': ','.join(DATA_PARAMS),
        'start': None,
        'end':  None
    }
PULL_FILEPATH ="/home/dori/Documents/Code/BestBeach/backend/analize/keysNdata/pulls.txt"
TIDE_API_PATH = 'https://api.stormglass.io/v2/tide/extremes/point'
FORECAST_API_PATH = 'https://api.stormglass.io/v2/weather/point'
HALF_MOON_DAY = timedelta(0, 0, 0, 0, 12.5, 6, 0)


def pull_data(forecast_type: str, timed:datetime = datetime.now(timezone.utc)) -> dict:
    """
    pulls the data from the stormglass API and saves it to a file
    :param forecast_type: str, either "surf" or "tide"
    :param timed: datetime object, the time to pull data for
    :return: dictionary of the data
    :raise: ValueError if forecast_type is not "surf" or "tide"
    :raise: TimeoutError if the request times out
    :raise: ConnectionError if there is a connection error
    """
    if forecast_type == "surf":
        PULL_PARAMS['start'], PULL_PARAMS['end'] = timed, timed
        api_path = FORECAST_API_PATH
    elif forecast_type == "tide":
        PULL_PARAMS['start'] = timed - HALF_MOON_DAY
        PULL_PARAMS['end'] = timed + HALF_MOON_DAY
        api_path = TIDE_API_PATH
    else:
        raise ValueError("Invalid forecast type. Use 'surf' or 'tide'.")
    try:
        response = requests.get(api_path, params=PULL_PARAMS,
                                headers={'Authorization': ACCESS_KEY}, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout as e:
        raise TimeoutError("The request timed out. Please try again later.") from e
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"An error occurred while making the request: {e}") from e
    res = response.json()
    with open(PULL_FILEPATH, 'a', encoding='utf-8') as f:
        f.write(str(res))
    return res


# makes a dictionary of the desired sea conditions
def sea_dict(timed: datetime = datetime.now(timezone.utc)) -> dict:
    """
    Pulls the data from the stormglass API and returns a dictionary of the desired sea conditions
    If relevant updates the collumn to be a median of the data
    :param timed: datetime object, the time to pull data for
    :return: dictionary of the data
    """

    # Reference data for testing, uncomment to use
    # x = {'hours':
    # [{
    #     'swellDirection': {'dwd': 271.02, 'icon': 268.68, 'noaa': 283.05, 'sg': 268.68},
    #     'swellHeight': {'dwd': 1.98, 'icon': 1.83, 'noaa': 0.35, 'sg': 1.83},
    #     'swellPeriod': {'dwd': 7.11, 'icon': 7.51, 'noaa': 7.64, 'sg': 7.51},
    #     'time': '2023-01-31T10:00:00+00:00',
    #     'windDirection': {'icon': 274.46, 'noaa': 279.5, 'sg': 274.46},
    #     'windSpeed': {'icon': 8.51, 'noaa': 8.3, 'sg': 8.51}
    # }],
    # 'meta':
    # {
    #     'cost': 1, 'dailyQuota': 10, 'end': '2023-01-31 10:20', 'lat': 32.1761, 'lng': 34.7984,
    #     'params': ['windSpeed', 'windDirection', 'swellHeight', 'swellDirection', 'swellPeriod'],
    #     'requestCount': 10, 'start': '2023-01-31 10:00'
    # }}
    # df = pd.DataFrame(x["hours"][0])

    df = pd.DataFrame(pull_data("surf", timed)["hours"][0])
    mean_val = {}
    columns = list(df)
    for col in columns:
        if col == "windSpeed":
            mean_val[col] = df[col].median()
        elif col == "windDirection" | "swellHeight" | "swellDirections" | "swellPeriod":
            mean_val[col] = df[col]["sg"]
    return mean_val


def get_tide(timed: datetime = datetime.now(timezone.utc)) -> int:
    """
    Pulls the tide data from the stormglass API and returns the tide situation
    as a trinary value
    :param timed: datetime object, the time to pull data for
    :return: 1 for high tide, -1 for low tide, 0 for mid-tide
    """
    d_tide = pull_data("tide", timed)["data"]
    #  Reference data for testing, uncomment to use
    # d_tide = [
    # {'height': 0.012778267802382953, 'time': '2023-02-07T06:04:00+00:00', 'type': 'high'},
    # {'height': -0.0261013218364069, 'time': '2023-02-07T10:43:00+00:00', 'type': 'low'},
    # {'height': 0.08379443397049985, 'time': '2023-02-07T17:25:00+00:00', 'type': 'high'}
    # ]
    # Default values
    min_delta = 7*3600
    tide_state = 0
    for i in d_tide:
        duration = datetime.strptime(i["time"],'%Y-%m-%dT%H:%M:%S%z')-timed
        delta = abs(duration.total_seconds())
        if delta<min_delta:
            if i["type"] == 'high':
                tide_state = 1
            else:
                tide_state = -1
            min_delta = delta
    # If tide is not high or low, return 0,
    # calculated by the time difference from the last high tide
    if 90 < abs(divmod(min_delta, 60)[0]) < 282:
        return 0
    return tide_state


def day_list(timed:datetime = datetime.now(timezone.utc)) -> pd.DataFrame:
    """
    Returns "Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide" for chosen time
    :param timed: datetime object, the time to pull data for
    :return: list of the data
    """
    df = pd.DataFrame.from_dict(sea_dict(timed))
    df["Tide"] = get_tide(timed)
    return df
