import numpy as np


def RMSE(y_true, y_pred):
    return np.sqrt(((y_true - y_pred) ** 2).mean(axis=-1))
