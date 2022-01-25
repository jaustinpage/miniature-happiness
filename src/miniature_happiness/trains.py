from contextlib import suppress
from typing import List

from flask import Blueprint, jsonify, request

from miniature_happiness.db_interfaces import (
    get_next_conflict,
    get_train_schedule,
    update_train_schedule,
)
from miniature_happiness.shapes import TrainSchedule

trains = Blueprint("trains", __name__)


@trains.route("/trains", methods=["POST"])
def add_train():
    """Implement a route that adds a train line"""
    train_json = request.get_json()
    train_shape = TrainSchedule(**train_json)
    update_train_schedule(train_shape)
    return "OK"


@trains.route("/trains/<string:train_id>")
def get_schedule(train_id):
    """Implement a route that returns the schedule for a given train line"""
    return jsonify(list(get_train_schedule(train_id).schedule))


@trains.route("/trains/next")
def get_next():
    """Implement a route that returns the next time multiple trains are in the
    station
    """
    return str(get_next_conflict(int(request.args.get("time", default="0"))))
