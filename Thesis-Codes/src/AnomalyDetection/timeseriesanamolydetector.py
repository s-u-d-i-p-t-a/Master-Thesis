import datetime
import json
import time
import dateparser
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from collections import OrderedDict
from numpy import *
from raiseanomaly import AnomalyDetection


# Handling data for the Anomaly Detection Algorithm

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


# Plotting anomalies in graph

converted_dates = map(datetime.datetime.strptime, xar, len(xar)*['%Y-%m-%dT%H:%M:%SZ'])
x_axis = converted_dates
fig = plt.figure()
plt.plot(x_axis, avg, 'g')


model = AnomalyDetection(avg, x_axis)    #Instantiate the object of Anomaly Detection class and call the main function to detect anomalies
residual, seasonality, trend, anomalies = model.detect_anomalies(avg, 1, len(avg), 0.02)

days = mdates.DayLocator()
hours = mdates.HourLocator(interval=2)
fig.autofmt_xdate()
ax = plt.gcf().axes[0]
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.xlabel('Time')
plt.ylabel('CPU Utilization')
plt.title('Plotting Time series data')
plt.legend(['Average'])


circle_rad = 2  # This is the radius, in points
for anomalyVal, index, score in anomalies:
    ax.plot(x_axis[index], anomalyVal, 'o', ms=circle_rad * 2, mec='r', mfc='none', mew=2)


# Plotting the trend of time series
fig2 = plt.figure()
ax1 = fig2.add_subplot(311)
ax1.set_title("Trend")
fig2.subplots_adjust(hspace=.5)
ax1.plot(trend)

# Plotting the residual of time series
ax2 = fig2.add_subplot(312)
ax2.set_title("Residual")
fig2.subplots_adjust(hspace=.5)
ax2.plot(residual)

# Plotting the seasonality of time series
ax3 = fig2.add_subplot(313)
ax3.set_title("Seasonality")
fig2.subplots_adjust(hspace=.5)
ax3.plot(seasonality)

# Display the plots
plt.show()


