# ヘルパー関数をまとめる
import numpy as np
def MAE(pred, true):
    return np.mean(np.abs(pred - true), axis=1)