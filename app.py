from flask import Flask, Response, jsonify, request

from db import Database

app = Flask(__name__)
db = Database()


@app.route('/')
def init():
    return "OK"


@app.route('/trains', methods=['POST'])
def add_train():
    """ Implement a route that adds a train line """
    raise NotImplementedError


@app.route('/trains/<string:train_id>')
def get_schedule(train_id):
    """ Implement a route that returns the schedule for a given train line """
    raise NotImplementedError


@app.route('/trains/next')
def get_next():
    """ Implement a route that returns the next time multiple trains are in the station """
    raise NotImplementedError


if __name__ == '__main__':
    app.run()
