from flask import Flask
import flask
from eklima import Station
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World"

@app.route('/temperature')
def temperature():
    retriever = Station('19710')
    return flask.jsonify(retriever.getDailyTemp('2016-05-19', '2016-06-20'))


if __name__ == '__main__':
    app.debug = True
    app.run()