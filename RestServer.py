from datetime import date
from flask import Flask
from flask import request
from flask_hal import HAL, document
from flask_hal.link import Collection, Link
import flask
import utm
from eklima import Station
from eklima import MetHistory
from utm.error import OutOfRangeError

app = Flask(__name__)
HAL(app)

@app.route('/')
def main():
    url_root = request.url_root
#     info = {'_links' : {'stations' : {'href' : url_root + 'stations/'}}}
#     return flask.jsonify(info)
    l = Collection(Link('stations', url_root + 'stations'))
    return document.Document(data={'message' : 'Based on data from met.no'},
                             links=l)


@app.route('/stations/')
def stations():
    base_url = request.base_url
    met_history = MetHistory()
    stations = met_history.getStationsWithHourlyTemperature()
    for station in stations:
        print "id={0}, utm= {1}".format(station['id'], station['pos_utm'])
        l = Collection(Link('self', base_url + station['id']), Link('temperatures', base_url + station['id'] + "/temperatures" ),
                       Link('googleMaps', utmToGoogleMapUrl(station['pos_utm'])))
        station['_links'] = l.to_dict()['_links']
    return document.Document(data={'stations' : stations})

@app.route('/stations/<stationId>', methods=['GET'])
def stationGet(stationId):
    base_url = request.base_url
    retriever = Station(stationId)    
    station = retriever.getProperties()
    l = Collection(Link('temperatures', base_url + "/temperatures" ),
                   Link('googleMaps', utmToGoogleMapUrl(station['pos_utm'])))
    return document.Document(data={'station' : station}, links=l)

    
@app.route('/stations/<stationId>/temperatures/', methods=['GET'])
def temperaturesGet(stationId):
    retriever = Station(stationId)
    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    specificDate = request.args.get('specificDate')
    if fromDate and toDate:        
        return flask.jsonify(retriever.getDailyTemp(fromDate, toDate))
    elif specificDate:
        return flask.jsonify(retriever.getHourlyTemp(specificDate))
    else:
        todayIso = date.today().isoformat()
        return flask.jsonify(retriever.getHourlyTemp(todayIso))


def utmToGoogleMapUrl(pos_utm):
    try:
        latLong = utm.to_latlon(int(pos_utm['east']), int(pos_utm['north']), int(pos_utm['zone']), northern=True)
        googleMapUrl = 'http://maps.google.com/maps?' + 'z=18' + "&" + 'q=loc:' + str(latLong[0]) + "+" + str(latLong[1])
        return googleMapUrl
    except OutOfRangeError:
        print ("Failed conversion" + str(pos_utm))
        return ""


if __name__ == '__main__':
    app.debug = True
    app.run()