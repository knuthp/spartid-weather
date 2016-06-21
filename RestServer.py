from flask import Flask
from flask import request
import flask
from eklima import Station
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World"

@app.route('/stations/<stationId>/temperatures/', methods=['GET'])
def temperatureDaily(stationId):
    retriever = Station(stationId)
    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    date = request.args.get('date')
    if fromDate and toDate:        
        return flask.jsonify(retriever.getDailyTemp(fromDate, toDate))
    elif date:
        return flask.jsonify(retriever.getHourlyTemp(date))
    else:
        return flask.jsonify(retriever.getHourlyTemp('2016-06-21'))


if __name__ == '__main__':
    app.debug = True
    app.run()