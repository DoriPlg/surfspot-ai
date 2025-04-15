"""
This module contains the code for updating the models, either from the database
or from a *.csv file.
"""
import pandas as pd
import pymongo
import model as mdl


def update_model_from_db(beach: str, db: pymongo) -> None:
    """
    Updates the model from the database
    :param beach: name of the beach for which the model is trained
    :param db: database connection
    """
    try:
        data = db["Sharon Beaches"]
        data = list(data.find({"Beach": beach}))
        # Maybe another movement is needed?

        update_model(beach, data)
    except pymongo.errors.ConnectionFailure as e:
        raise SystemError("Trouble connecting to server") from e

def update_model_from_csv(beach: str, csv_path: str) -> None:
    """
    Updates the model from the csv file
    :param beach: name of the beach for which the model is trained
    :param csv_path: path to the csv file
    """
    try:
        data = pd.read_csv(csv_path)
        update_model(beach, data)
    except FileNotFoundError as e:
        raise SystemError("File not found") from e

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
