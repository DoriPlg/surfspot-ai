"""
This module is responsible for evaluating which features are most important for the model.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model import prepare_data

def feature_evaluation(attributes: pd.DataFrame, target: pd.Series, output_path: str = "."):
    """
    Create scatter plot between each feature and the response.
        - Plot title specifies feature name
        - Plot title specifies Pearson Correlation between feature and response
        - Plot saved under given folder with file name including feature name
    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Design matrix of regression problem

    y : array-like of shape (n_samples, )
        Response vector to evaluate against

    output_path: str (default ".")
        Path to folder in which plots are saved
    """
    for feat in attributes.columns:
        correlation = attributes[feat].corr(target, method="pearson")
        plt.figure(figsize=(8, 6))
        plt.scatter(attributes[feat], target, alpha=0.5, label="Data Points")
        m, b = np.polyfit(attributes[feat], target, 1)
        plt.plot(attributes[feat], m * attributes[feat] + b, color="red", label="Fit Line")
        plt.title(f"{feat} vs Rating\nPearson Correlation: {correlation:.2f}")
        plt.xlabel(feat)
        plt.ylabel("Rating")
        plt.legend()
        plt.savefig(f"{output_path}/{feat}_correlation.png")
        plt.close()

if __name__=="main":
    data = prepare_data(pd.read_csv("data.csv"))
    X = data.drop(columns=["Rating"])
    y = data["Rating"]
    feature_evaluation(X, y, output_path="feature_evaluation")
