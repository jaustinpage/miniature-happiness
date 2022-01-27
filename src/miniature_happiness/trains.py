from flask import Blueprint, Response, jsonify, request

from miniature_happiness.db_interfaces import (
    get_next_conflict,
    get_train_schedule,
    update_train_schedule,
)
from miniature_happiness.shapes import TrainSchedule

trains = Blueprint("trains", __name__)


@trains.route("/trains", methods=["POST"])
def add_train() -> str:
    """Implement a route that adds a train line

    :returns: OK string if successful
    """
    train_json = request.get_json() or {}
    train_shape = TrainSchedule(**train_json)
    update_train_schedule(train_shape)
    return "OK"


@trains.route("/trains/<string:train_id>")
def get_schedule(train_id: str) -> Response:
    """Implement a route that returns the schedule for a given train line

    :param train_id: the id of the train to get
    :returns: the schedule for a train_id
    """

    return jsonify(list(get_train_schedule(train_id).schedule))


@trains.route("/trains/next")
def get_next() -> str:
    """Implement a route that returns the next time multiple trains are in the
    station

    :returns: String that is the next time multiple trains are in the station
    """
    return str(get_next_conflict(int(request.args.get("time", default="0"))))
