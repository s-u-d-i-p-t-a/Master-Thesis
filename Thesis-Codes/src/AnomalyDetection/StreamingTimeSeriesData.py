import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import dateparser
import json
import matplotlib.dates as mdates
from collections import OrderedDict
import datetime

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def loadData(filename):
    with open(filename) as data_file:
        return json.load(data_file, object_pairs_hook=OrderedDict)

def animate(i):
    dataStream = loadData('data/sampleText.txt')
    sorted_obj = dict(dataStream)
    sorted_obj['Datapoints'] = sorted(dataStream['Datapoints'], key=lambda x: int(time.mktime(dateparser.parse(x['Timestamp']).timetuple())), reverse=False)

    xar = []
    yar = []
    for data in sorted_obj["Datapoints"]:
        for attribute in data:
            if attribute == "Timestamp":
                dt = dateparser.parse(data[attribute])
                timestamp = int(time.mktime(dt.timetuple()))
                xar.append(timestamp)
                #print datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            if attribute == "Minimum":
                yar.append(data[attribute])

    xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    ax1.clear()
    ax1.plot(xar,yar)


ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()