import plotly.graph_objs as go
import plotly 
from eklima import Station, MetHistory
import dateutil.parser
from datetime import datetime

class GraphTemp:
    def daily(self, stationProperties, data):
        x = []
        minArr = []
        maxArr = []
        meanArr = []
        for elem in data:
            dayAndTime = dateutil.parser.parse(elem['time'])
            x.append(dayAndTime)
            minArr.append(elem['values']['minimum'])
            maxArr.append(elem['values']['maximum'])
            meanArr.append(elem['values']['mean'])
        
        
        trace1 = go.Scatter(name='Min', x=x, y=minArr) 
        trace2 = go.Scatter(name='Max', x=x, y=maxArr)
        trace3 = go.Scatter(name='Mean', x=x, y=meanArr)
        data = [trace1, trace2, trace3]
        layout = go.Layout(title=stationProperties['name'] + " from=" + str(x[0]) + " to=" + str(x[len(x) - 1]))
        plotly.offline.plot({'data' : data, 'layout' : layout}, filename='timeseries.html', )


station = Station('19710')
data = station.getDailyTemp('2015-01-01', '2016-01-01')

graphTemp = GraphTemp()
graphTemp.daily(station.getProperties(), data);

