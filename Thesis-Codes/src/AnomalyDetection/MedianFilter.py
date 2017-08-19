from numpy import *
import scipy as sp
import matplotlib.pyplot as plt
from scipy import signal
from statsmodels.robust.scale import mad


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

t = linspace(0, 10, 200)  # create a time signal
x1 = sin(t)  # create a simple sine wave
x2 = x1 + random.rand(200)  # add noise to the signal
y1 = sp.signal.medfilt(x2, 25)  # add noise to the signal
print find_mad_based_outlier(y1, 2.5)

# plot the results
plt.subplot(2, 1, 1)
plt.plot(t, x2, 'yo-')
plt.title('input wave')
plt.xlabel('time')
plt.subplot(2, 1, 2)
plt.plot(range(200), y1, 'yo-')
plt.title('filtered wave')
plt.xlabel('time')
plt.show()