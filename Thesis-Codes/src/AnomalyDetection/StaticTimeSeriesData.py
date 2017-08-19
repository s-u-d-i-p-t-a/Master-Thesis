import datetime
import json
import time
import dateparser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from collections import OrderedDict
from numpy import *


def loadData(filename):
    with open(filename) as data_file:
        return json.load(data_file, object_pairs_hook=OrderedDict)


def createDataMap(data, type):
    datamap = {}
    for dataItr in data["Datapoints"]:
        datamap[dataItr["Timestamp"]] = dataItr[type]
    return datamap


dataStream_min = loadData('data/cloudwatch-CPUUtilization-Minimum.json')
dataStream_max = loadData('data/cloudwatch-CPUUtilization-Maximum.json')
dataStream_avg = loadData('data/cloudwatch-CPUUtilization-Average.json')

sorted_obj_min = dict(dataStream_min)
sorted_obj_max = dict(dataStream_max)
sorted_obj_avg = dict(dataStream_avg)
sorted_obj_min['Datapoints'] = sorted(dataStream_min['Datapoints'], key=lambda x: int(time.mktime(dateparser.parse(x['Timestamp']).timetuple())), reverse=False)

datamap_obj_max = createDataMap(sorted_obj_max, "Maximum")
datamap_obj_avg = createDataMap(sorted_obj_avg, "Average")

xar = []
max = []
min = []
avg = []

for data in sorted_obj_min["Datapoints"]:
    for attribute in data:
        if attribute == "Timestamp":
            xar.append(data[attribute])
            max.append(datamap_obj_max[data[attribute]])
            avg.append(datamap_obj_avg[data[attribute]])
            #print dt.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        if attribute == "Minimum":
            min.append(data[attribute])

# Anomaly detection algorithm with the data

converted_dates = map(datetime.datetime.strptime, xar, len(xar)*['%Y-%m-%dT%H:%M:%SZ'])
x_axis = (converted_dates)
fig = plt.figure()
plt.plot(x_axis, max,'r')
plt.plot(x_axis, min,'b')
plt.plot(x_axis, avg,'g')

# Code for anomaly here to plot in graph

days = mdates.DayLocator()
hours = mdates.HourLocator(interval=3)
dfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()
ax = plt.gcf().axes[0]
ax.xaxis.set_major_formatter(dfmt)
plt.xlabel('Time')
plt.ylabel('CPU Utilization')
plt.title('Plotting Time series data')
plt.legend(['Maximum', 'Minimum', 'Average'])
plt.subplots_adjust(bottom=.30)

plt.show()