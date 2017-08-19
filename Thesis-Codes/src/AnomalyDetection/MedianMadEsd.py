from numpy import *
from statsmodels.robust.scale import mad
from PyAstronomy import pyasl


def find_median(data):

    if len(data) < 1:
        return None
    return median(data)


def find_mad(data):

    if len(data) < 1:
        return None
    else:
        return mad(data, c=0.6745, axis=0, center=median(data))


def find_mad_based_outlier(data, thresh):

    if len(data) < 1:
        return None
    else:
        outlier_score = abs(data-median(data))/find_mad(data)

    return outlier_score > thresh


def apply_generalizedESD(dataframe, column_name, max_num_outliers=10,
                         significance=0.05):
    array = dataframe[column_name]
    r = pyasl.generalizedESD(array, max_num_outliers,
                             significance, fullOutput=True)


# x = [10, 12, 3, 4, 1]
# print find_median(x)
# print find_mad(x)

x = [90, 90, 90, 90, 90, 90]

print find_mad_based_outlier(x, 3.5)


