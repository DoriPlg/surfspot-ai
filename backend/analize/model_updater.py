"""
This module contains the code for updating the models, either from the database
or from a *.csv file.
"""
import pandas as pd
import pymongo
import model as mdl


def update_model_from_db(beach: str, db: pymongo.MongoClient) -> None:
    """
    Updates the model from the database
    :param beach: name of the beach for which the model is trained
    :param db: database connection
    :raises ConnectionError: if the connection to the database fails
    """
    try:
        data = db["Sharon Beaches"]
        data = data.find({"Beach": beach})
        # Maybe another movement is needed?

        update_model(beach, list(data))
    except pymongo.errors.ConnectionFailure as e:
        raise ConnectionError("Trouble connecting to server") from e

def update_model_from_csv(beach: str, csv_path: str) -> None:
    """
    Updates the model from the csv file
    :param beach: name of the beach for which the model is trained
    :param csv_path: path to the csv file
    :raises FileNotFoundError: if the file is not found
    """
    try:
        data = pd.read_csv(csv_path)
        update_model(beach, data)
    except FileNotFoundError as e:
        raise FileNotFoundError("File not found") from e

def update_model(beach: str, data: pd.DataFrame) -> None:
    """
    Updates the model from the given data
    :param beach: name of the beach for which the model is trained
    :param data: DataFrame to train on
    """
    try:
        mdl.save_model(mdl.train_model(data), beach)
    except ValueError as e:
        raise SystemError("Data not valid") from e
