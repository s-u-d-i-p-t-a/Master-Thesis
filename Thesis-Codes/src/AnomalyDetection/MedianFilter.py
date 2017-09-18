from numpy import *
import scipy as sp
import matplotlib.pyplot as plt
from scipy import signal
from statsmodels.robust.scale import mad
from scipy.signal import medfilt

def find_mad_based_outlier(data, thresh):

    if len(data) < 1:
        return None
    else:
        z_score = abs(data - median(data)) / find_mad(data)

    return z_score > thresh


def find_mad(data):

    if len(data) < 1:
        return None
    else:
        return mad(data, c=0.6745, axis=0, center=median(data))

print(medfilt([2, 6, 5, 4,0,3,5,7,9,2,0,1], 5))