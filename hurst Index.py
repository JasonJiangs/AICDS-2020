# -*- coding: utf-8 -*-
# @Time : 2020/12/19 23:25 
# @Author : Jason
# @File : hurst Index.py 
# @Software: PyCharm
import numpy as np
import pandas as pd


def Hurst(data):
    n = 6
    data = pd.Series(data).pct_change()[1:]
    ARS = list()
    lag = list()
    for i in range(n):
        m = 2 ** i
        size = np.size(data) // m
        lag.append(size)
        panel = {}
        for j in range(m):
            panel[str(j)] = data[j*size:(j+1)*size].values

        panel = pd.DataFrame(panel)
        mean = panel.mean()
        Deviation = (panel - mean).cumsum()
        maxi = Deviation.max()
        mini = Deviation.min()
        sigma = panel.std()
        RS = maxi - mini
        RS = RS / sigma
        ARS.append(RS.mean())

    lag = np.log10(lag)
    ARS = np.log10(ARS)
    hurst_exponent = np.polyfit(lag, ARS, 1)
    hurst = hurst_exponent[0]

    return hurst


nDate = pd.read_csv('C:/Users/dcdn/Desktop/HS300_Data3.csv')
hurst = Hurst(nDate['CPrice'])
print(hurst)