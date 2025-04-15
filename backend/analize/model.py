"""
This module contains the code for training and predicting the model
"""
import pandas as pd
import numpy as np
import sklearn.linear_model as linear_model
from skl2onnx import to_onnx
from utils import wind_dir

CORE_ATTRIBUTES = ["Wind Sp", "Wind Dir", "Swell Hgt", "Swell Dir", "Swell Prd", "Tide"]
USED_ATTRIBUTES = ["Wind Qual", "Wind Dir^2", "Wind Dir^3","Tide^2"] + CORE_ATTRIBUTES

def prepare_data(data:pd.DataFrame)->pd.DataFrame:
    """
    Prepares the data for training by cleaning and transforming it
    :param data: DataFrame to prepare
    :return: cleaned and transformed DataFrame
    :raises AttributeError: if the data does not contain the required attributes
    """
    # Clean the data
    data = data.dropna()
    for attr in CORE_ATTRIBUTES:
        if attr not in data.columns:
            raise AttributeError(f"Missing attribute {attr} in data")

    # Transform the data
    data["Wind Qual"] = np.zeros(len(data))
    for i in range(len(data)):
        data["Wind Qual"][i] = data["Wind Sp"][i] * wind_dir(data["Wind Dir"][i])
    data["Wind Dir^2"] = data["Wind Dir"]**2
    data["Wind Dir^3"] = data["Wind Dir"]**3 # Careful not to overfit (?)
    data["Tide^2"] = data["Tide"]**2

    return data

def train_model(data:pd.DataFrame) -> linear_model.LinearRegression:
    """
    Trains a linear regression model on the given data
    :param data: DataFrame to train on
    :return: trained model
    """
    data = prepare_data(data)
    X = data[USED_ATTRIBUTES]
    y = data["Rating"]
    # Intercept, because a bad day surfing beats a good day at work
    model = linear_model.LinearRegression(fit_intercept=True)
    model.fit(X.values, y)
    return model


def save_model(model:linear_model.LinearRegression, beach:str) -> None:
    """
    Saves the model to a file
    :param model: trained model
    :param beach: name of the beach for which the model is trained
    """
    onx = to_onnx(model, X=None, initial_types=np.float32, target_opset=12)
    with open(f"{beach}.onnx", "wb") as f:
        f.write(onx.SerializeToString())

def load_model(beach:str) -> linear_model.LinearRegression:
    """
    Loads the model from a file
    :param beach: name of the beach for which the model is trained
    :return: loaded model
    :raises FileNotFoundError: if the model file is not found
    """
    try:
        with open(f"{beach}.onnx", "rb") as f:
            onx = f.read()
        return onx
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Model for beach {beach} not found. Please train the model first.") from exc

def predict(conditions:pd.DataFrame, beach:str) -> float:
    """
    Predicts the rating for the given conditions using the trained model
    :param conditions: DataFrame of conditions [Wind Sp, Wind Dir, Swell Hgt, Swell Dir, Swell Prd]
    :param beach: name of the beach for which the model is trained
    :return: predicted rating
    """
    model = load_model(beach)
    data = prepare_data(conditions)
    return model.predict(data[USED_ATTRIBUTES].values)[0]
