import plotly.graph_objs as go
import plotly 
from eklima import Station
import dateutil.parser
from datetime import datetime

station = Station('19710')
data = station.getDailyTemp('2015-01-01', '2016-01-01')

x = []
minArr = []
maxArr = []
for elem in data:
    dayAndTime = dateutil.parser.parse(elem['time'])
    x.append(dayAndTime)
    minArr.append(elem['values']['minimum'])
    maxArr.append(elem['values']['maximum'])


trace1 = go.Scatter(name='Min', x=x, y=minArr) 
trace2 = go.Scatter(name='Max', x=x, y=maxArr)
data = [trace1, trace2]
plotly.offline.plot(data, filename='timeseries.html')
