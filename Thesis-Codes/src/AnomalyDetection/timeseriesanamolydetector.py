import datetime
import json
import time
import dateparser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from collections import OrderedDict
from numpy import *
import madgsd as model
from madgsd import MADGSDAnamoly


def loadData(filename):
    with open(filename) as data_file:
        return json.load(data_file, object_pairs_hook=OrderedDict)

def createDataMap(data, type):
    datamap = {}
    for dataItr in data["Datapoints"]:
        datamap[dataItr["Timestamp"]] = dataItr[type]
    return datamap

dataStream_avg = loadData('data/cloudwatch-CPUUtilization-Average.json')

sorted_obj_avg = dict(dataStream_avg)
sorted_obj_avg['Datapoints'] = sorted(dataStream_avg['Datapoints'], key=lambda x: int(time.mktime(dateparser.parse(x['Timestamp']).timetuple())), reverse=False)
datamap_obj_avg = createDataMap(sorted_obj_avg, "Average")

xar = []
avg = []

for data in sorted_obj_avg["Datapoints"]:
    for attribute in data:
        if attribute == "Timestamp":
            xar.append(data[attribute])
            avg.append(datamap_obj_avg[data[attribute]])

# Anomaly detection algorithm with the data

converted_dates = map(datetime.datetime.strptime, xar, len(xar)*['%Y-%m-%dT%H:%M:%SZ'])
x_axis = (converted_dates)
fig = plt.figure()
plt.plot(x_axis, avg,'g')

# Code for anomaly here to plot in graph
model = MADGSDAnamoly(avg, x_axis)
anomalies = model.detect_series(avg, 1, len(avg))

days = mdates.DayLocator()
hours = mdates.HourLocator(interval=2)
fig.autofmt_xdate()
ax = plt.gcf().axes[0]
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.xlabel('Time')
plt.ylabel('CPU Utilization')
plt.title('Plotting Time series data')
plt.legend(['Average'])
plt.subplots_adjust(bottom=.30)

circle_rad = 2  # This is the radius, in points
for anamolyVal, index, score in anomalies:
    ax.plot(x_axis[index], anamolyVal, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)

plt.show()