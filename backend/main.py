import pandas as pd
# import matplotlib.pyplot as plt
import numpy.random as rnd
from sklearn import linear_model
# import numpy
import copy
pd.set_option('display.max_columns', None)


beach_names = ["Pirza", "Marina main", "Marina bath", "Marina open", "Gazibo", "9Beach", "Sidni Ali", "Gaash"]


# returns ordinal wind direction, probably useless
def wind_dir(deg):
    while deg > 360 or deg < 0:
        if deg > 360:
            deg -= 360
        if deg < 0:
            deg += 360
    if 325 >= deg >= 245:
        return "On-shore"
    elif 140 >= deg >= 70:
        return "Off-shore"
    else:
        return "Cross-shore"


# creates random data table, to work with. NO CORRELATION TO REALITY
def make_table(size=300):
    beach = []
    for i in range(size):
        beach.append(beach_names[rnd.randint(0, len(beach_names))])
    tide = rnd.randint(-1, 3, size)
    for i in range(len(tide)):
        if tide[i] == 1: tide[i] = 0
        if tide[i] == 2: tide[i] = 1
    actual = rnd.normal(5, 2, size)
    for i in range(len(actual)):
        actual[i] = round(actual[i], 0)
        if actual[i] > 7:
            actual[i] = 7
        if actual[i] < 0:
            actual[i] = 0
    wind_s = rnd.normal(12, 4.3, size)
    for i in range(len(wind_s)): wind_s[i] = round(wind_s[i], 1)
    wind_d = rnd.normal(280, 100, size)
    for i in range(len(wind_d)):
        wind_d[i] = round(wind_d[i], 0)
        if wind_d[i] > 360:
            wind_d[i] -= 360
        if wind_d[i] < 0:
            wind_d[i] += 360
    swell_h = rnd.normal(1.3, 0.4, size)
    for i in range(len(swell_h)): swell_h[i] = round(swell_h[i], 2)
    swell_d = rnd.normal(280, 10, size)
    for i in range(len(swell_d)):
        swell_d[i] = round(swell_d[i], 0)
        if swell_d[i] > 360:
            swell_d[i] = 360
        if swell_d[i] < 200:
            swell_d[i] = 200
    swell_p = rnd.normal(8.0, 1.5, size)
    for i in range(len(swell_p)): swell_p[i] = round(swell_p[i], 0)
    tab = {
        "Beach": beach,
        "Tide": tide,
        "Wind Sp": wind_s,
        "Wind Dir": wind_d,
        "Swell Hgt": swell_h,
        "Swell Dir": swell_d,
        "Swell Prd": swell_p,
        "Actual": actual
    }
    return pd.DataFrame(tab)


# returns the foreseen "actual" rating for certain conditions, in a certain beach, in a given dataframe
def rate_for_current(today: list, beach: str, main_data: pd.DataFrame):  # switch to string when the time comes
    df = copy.copy(main_data)
    for x in df.index:
        if df.loc[x, "Tide"] != today[-1]:
            df.drop(x, inplace=True)
    print(df)
    for x in df.index:
        if df.loc[x, "Beach"] != beach:
            df.drop(x, inplace=True)
    X = df[["Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd"]]
    y = df["Actual"]
    """
    plt.scatter(df["Wind Sp"], y)
    plt.show()
    plt.scatter(df["Wind Dir"], y)
    plt.show()
    plt.scatter(df["Swell Hgt"], y)
    plt.show()
    plt.scatter(df["Swell Dir"], y)
    plt.show()
    plt.scatter(df["Swell Prd"], y)
    plt.show()
    """
    regress = linear_model.LinearRegression()
    regress.fit(X.values, y)
    today = [today[0:-1:]]
    """
    Should tide be left? and treated as a linear non-dependent? or does it completely change the beach?
    """
    print(df)
    return regress.predict(today)


# returns sorted list of beaches and their rating
def best_list(conditions: list):
    cond_list = []
    global beach_names
    for i in beach_names:
        x = rate_for_current(conditions, i, grand)[0]
        print(x)
        a = 0
        try:
            while x < cond_list[a][1]:
                a += 1
            cond_list.insert(a, [i, x])
        except:
            cond_list.append([a, x])
    return cond_list


# creates a json file to use as the data source (fictive)
def update_json():
    grand = make_table(500)
    grand.to_json(r'~/Documents/Python/BestBeach/backend/GreatBigData.json')
    print("Done")


# update_json()
grand = pd.read_json('GreatBigData.json')
print(grand)
this_day = [4, 80, 1.3, 275, 8, 1]  # "Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide"
print(best_list(this_day))
