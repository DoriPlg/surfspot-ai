import numpy.random as rnd
import numpy as np
import pandas as pd


BEACH_NAMES = ["Marina main", "Gazibo", "9Beach", "Sidni Ali"]
ONSHORE = 280





def wind_dir(deg: float) -> int:
    """
    returns number representing wind direction in relation to shore
    it is possible to add finer tuning, or switch with polynomial regression altogether
    :param deg: wind direction in degrees
    :return: 1 - offshore, 2 - onshore, 3 - side-offshore, 4 - side-onshore
    """
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
        if 20 <= deg <= 190:
            return 3  # side-offshore
        return 4  # side-onshore


def random_beaches(size: int = 100) -> list:
    """
    Returns a list of random beaches
    :param size: number of beaches to return
    :return: list of beaches
    """
    beach = []
    beach_vector = rnd.randint(0, len(BEACH_NAMES), size=size)
    for i in range(size):
        beach.append(BEACH_NAMES[beach_vector[i]])
    return beach

def random_tides(size: int = 100) -> np.ndarray:
    """
    Returns a list of random tides
    :param size: number of tides to return
    :return: list of tides
    """
    return np.rint(rnd.normal(0, 0.5, size))

def random_ratings(size: int = 100) -> np.ndarray:
    """
    Returns a list of random ratings
    :param size: number of ratings to return
    :return: list of ratings
    """
    ratings = np.rint(rnd.normal(5, 2, size))
    for i in range(size):
        ratings[i] = round(ratings[i], 0)
        if ratings[i] > 7:
            ratings[i] = 7
        if ratings[i] < 1:
            ratings[i] = 1
    return ratings

def random_wind_conditions(size: int = 100) -> dict[str,np.ndarray]:
    """
    Returns a dictionary of random wind conditions
    :param size: number of wind conditions to return
    :return: dictionary of wind conditions, keyed by "Wind Sp", "Wind Dir", "Wind Qual"
    """
    wind_s = np.round(rnd.normal(12, 4.3, size),decimals=2)
    wind_d = rnd.normal(ONSHORE, 130, size)
    wind_q = []
    for i in range(size):
        wind_q.append(wind_dir(wind_d[i]) * wind_s[i])
    return {
        "Wind Sp": wind_s,
        "Wind Dir": wind_d,
        "Wind Qual": wind_q
    }

def random_swell(size: int = 100) -> dict[str,np.ndarray]:
    """
    Returns a dictionary of random swell conditions
    :param size: number of swell conditions to return
    :return: dictionary of swell conditions, keyed by "Swell Hgt", "Swell Dir", "Swell Prd"
    """
    swell_h = np.round(rnd.normal(1.3, 0.4, size),decimals=2)
    swell_d = np.round(rnd.normal(ONSHORE, 10, size), decimals=0)
    for i in range(size):
        swell_d[i] = min(swell_d[i], 360)
        swell_d[i] = max(swell_d[i],200)
    swell_p = rnd.normal(8.0, 1.5, size)
    for i in range(size):
        swell_p[i] = round(swell_p[i], 0)
    return {
        "Swell Hgt": swell_h,
        "Swell Dir": swell_d,
        "Swell Prd": swell_p
    }

def make_random_table(size:int=100)->pd.DataFrame:
    """
    Creates random data table, to work with. NO CORRELATION TO REALITY
    :param size: number of rows to create
    :return: DataFrame with random data
    """
    beach = random_beaches(size)
    tide = random_tides(size)
    ratings = random_ratings(size)
    wind = random_wind_conditions(size)
    swell = random_swell(size)
    tab = {
        "Beach": beach,
        "Tide": tide,
        "Actual": ratings
    }
    tab.update(wind)
    tab.update(swell)
    return pd.DataFrame(tab)
