"""
This is the main file for the backend of the Best Beach project.
It contains the FastAPI application and the main functions for handling requests.
"""
from datetime import datetime, timezone
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import model
import conditions
import database_handler as dhn
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
        raise SystemError(f"Model not found. Please train the model for {beach} first.")\
                            from exc

def best_list(weather_metrics: pd.DataFrame) -> dict[str, float]:
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
        x = rate_for_current(weather_metrics, beach)
        print("For", beach,'-', x)
        beach_conditions[beach] = x
    return beach_conditions


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

def parse_check_for(check_for) -> datetime:
    """
    Parses the check_for parameter to a datetime object
    :param check_for: datetime object or string in the format YYYY-MM-DD%20HH:mm
    :return: datetime object
    """
    if check_for == "NOW":
        check_for = datetime.now(timezone.utc)
    elif isinstance(check_for, str):
        check_for = change_time_zone(check_for)
    elif not isinstance(check_for, datetime):
        raise ValueError("Invalid date format from client. Use YYYY-MM-DD%20HH:mm or NOW")
    return check_for


@app.get("/numcrunch/{check_for}")
def sendlist(check_for = datetime.now(timezone.utc)) -> JSONResponse:
    """
    Returns calculated list of beaches for a given date-time string - formatted YYYY-MM-DD%20HH:mm
    :param check_for: datetime object or string in the format YYYY-MM-DD%20HH:mm
    :return: JSONResponse with the list of beaches and their rating
    """
    this_day = conditions.day_list(parse_check_for(check_for))
    try:
        return JSONResponse(content={"conditions": this_day.to_dict(),
                                 "beachList": best_list(this_day)})
    except DataError:
        return JSONResponse(content={"Error": "No beaches found"}, status_code=500)


@app.get("/conditions/{check_for}")
def cond_time(check_for = datetime.now(timezone.utc)):
    """
    Returns conditions for a given date-time string - formatted YYYY-MM-DD%20HH:mm
    :param check_for: datetime object or string in the format YYYY-MM-DD%20HH:mm
    :return: JSONResponse with the conditions for the given date-time
    """
    this_day = conditions.day_list(parse_check_for(check_for))
    return JSONResponse(content=this_day.to_dict())


@app.get("/addrev/datetime={date_time}&beach={beach}&rate={rate}")
def new_review(date_time: str, beach: str, rate: str) -> JSONResponse:
    """
    Adds a review to the database - time formatted YYYY-MM-DD%20HH:mm
    :param dateTime: datetime object or string in the format YYYY-MM-DD%20HH:mm
    :param beach: name of the beach
    :param rate: rating for the beach
    :return: JSONResponse with the response
    """
    try:
        client = dhn.connect_to_mongo()
    except FileNotFoundError as exc:
        return JSONResponse(content={"Error": exc}, status_code=500)
    except ConnectionError as exc:
        return JSONResponse(content={"Error": exc}, status_code=500)
    db = client["Reviews"]
    collection = db["From Web"]
    try:
        row = conditions.day_list(change_time_zone(date_time))
    except ValueError as exc:
        return JSONResponse(content={"Error": exc}, status_code=400)
    except TimeoutError as exc:
        return JSONResponse(content={"Error": exc}, status_code=408)
    except ConnectionError as exc:
        return JSONResponse(content={"Error": exc}, status_code=500)
    row["Rating"] = float(rate)
    row["Beach"] = beach
    collection.insert_one(row.to_dict())
    return JSONResponse(content={"Response":"Successfuly uploaded"})


@app.get("/which_beaches")
def beaches() -> JSONResponse:
    """
    Returns a list of beaches for which we have models
    :return: JSONResponse with the list of beaches
    """
    return JSONResponse(content={"Beaches":get_beaches()})


class DataError(Exception):
    """
    Custom exception for data errors
    """
