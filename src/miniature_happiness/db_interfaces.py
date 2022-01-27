from dataclasses import astuple
from typing import List, Union

from miniature_happiness.db import Database
from miniature_happiness.shapes import TimeSlot, TrainSchedule, is_time

d = Database()


class DbTypes:
    def __init__(self):
        self.types = {}

    def register(self, type):
        self.types[type.__name__] = type
        self.types[type] == type.__name__

    def get(self, db_type, key: str):
        try:
            value = d.get(f"{self.types[db_type.__name__]}:{key}")
            return db_type(key, value)
        except KeyError:
            raise ValueError(f"Unknown database type: {db_type.__name__}")

    def save(self, db_type_instance):
        key, value = astuple(db_type_instance)
        d.set(f"{self.types[type(db_type_instance)]}:{key}", value)

    def list(self, db_type):
        return {
            x.split(":", 1)[1] for x in d.keys() if x.startswith(f"{db_type.__name__}:")
        }


db = DbTypes()
db.register(TimeSlot)
db.register(TrainSchedule)


def get_train_schedule(train_id: str) -> TrainSchedule:
    """Get a train schedule from the database.

    :param train_id: The train id to get the schedule for.
    :returns: Train schedule.
    """
    schedule = d.get("train_id:" + train_id) or set()
    return TrainSchedule(id=train_id, schedule=schedule)


def save_train_schedule(train_schedule: TrainSchedule) -> None:
    """Save a train schedule to the database.

    :param train_schedule: The train schedule to store in the database.
    """
    d.set("train_id:" + train_schedule.id, train_schedule.schedule)


def list_train_schedules() -> List[str]:
    """Get a list of all the trains we have schedules for.

    :returns: List of all trains.
    """
    return [x.split(":", 1)[1] for x in d.keys() if x.startswith("train_id:")]


def get_time_slot(time: int) -> TimeSlot:
    """Get the trains arriving in a time slot for the station.

    :param time: Time slot to retrieve.
    :returns: Time slot.
    """
    trains = d.get("time:" + str(time)) or set()
    return TimeSlot(time=time, trains=trains)


def save_time_slot(time_slot: TimeSlot) -> None:
    """Save a time slot to the database.

    :param time_slot: the time slot to save to the database.
    """
    d.set("time:" + str(time_slot.time), time_slot.trains)


def list_time_slots() -> list[int]:
    """List the times that trains are arriving to the station.

    :returns: list of times when trains arrive.
    """
    return [int(x.split(":", 1)[1]) for x in d.keys() if x.startswith("time:")]


def update_train_schedule(train_schedule: TrainSchedule) -> None:
    """Update the schedule for a train in the database.

    :param train_schedule: The new train schedule to store.
    """
    old_train_schedule = get_train_schedule(train_schedule.id)
    time_slot_deletions = old_train_schedule.schedule.difference(
        train_schedule.schedule
    )
    time_slot_additions = train_schedule.schedule.difference(
        old_train_schedule.schedule
    )

    for time_slot in time_slot_deletions:
        time_slot_o = get_time_slot(time_slot)
        time_slot_o.trains.discard(train_schedule.id)
        save_time_slot(time_slot_o)

    for time_slot in time_slot_additions:
        time_slot_o = get_time_slot(time_slot)
        time_slot_o.trains.add(train_schedule.id)
        save_time_slot(time_slot_o)

    save_train_schedule(train_schedule)


def update_time_slot(time_slot: TimeSlot) -> None:
    """Update the trains arriving in a time slot for the database.

    :param time_slot: The time slot to update.
    """
    old_time_slot = get_time_slot(time_slot.time)
    train_schedule_deletions = old_time_slot.trains.difference(time_slot.trains)
    train_schedule_additions = time_slot.trains.difference(old_time_slot.trains)

    for train_schedule in train_schedule_deletions:
        train_schedule_o = get_train_schedule(train_schedule)
        train_schedule_o.schedule.discard(time_slot.time)
        save_train_schedule(train_schedule_o)

    for train_schedule in train_schedule_additions:
        train_schedule_o = get_train_schedule(train_schedule)
        train_schedule_o.schedule.add(time_slot.time)
        save_train_schedule(train_schedule_o)

    save_time_slot(time_slot)


def get_next_conflict(
    start_time: int = 1, number_of_trains: int = 2
) -> Union[int, None]:
    start_time = is_time(start_time)

    # max number of time slots is 24hr * 60min
    time_slots = sorted(list_time_slots())

    # rotate the list to start at the first time after the indicated time.
    index = 0
    for i, time in enumerate(time_slots):
        if time >= start_time:
            index = i
            break

    time_slots_rotated = time_slots[index:] + time_slots[:index]

    for time in time_slots_rotated:
        if len(get_time_slot(time).trains) >= number_of_trains:
            return time
    return None
