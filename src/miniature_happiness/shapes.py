from dataclasses import dataclass, field
from typing import List, Set, Union


def is_time(time: Union[int, str]):
    time = int(time)

    if not 0 <= time < 2400:
        raise ValueError("hours must be between 0 and 24")

    if not 0 <= time % 100 < 60:
        raise ValueError("minutes must be between 0 and 60")

    return time


def is_schedule(schedule: Union[List[Union[int, str]], Set[Union[int, str]]]):
    schedule = schedule or set()
    schedule = {is_time(t) for t in schedule}
    schedule.discard(None)
    return schedule or set()


def is_train_id(train_id: str):
    if not isinstance(train_id, str):
        raise ValueError("Must provide train_id as a string")

    if not train_id.isalnum():
        raise ValueError("train id must be alphanumeric")

    if not 0 < len(train_id) <= 4:
        raise ValueError("train id must be 1 to 4 characters long")

    return train_id


def is_trains(trains: Union[List[Union[int, str]], Set[Union[int, str]]]):
    trains = trains or set()
    trains = {is_train_id(t) for t in trains}
    trains.discard(None)
    return trains or set()


@dataclass
class TrainSchedule:
    id: str
    schedule: Set[int] = field(default_factory=set)

    def __post_init__(self):
        self.id = is_train_id(self.id)
        self.schedule = is_schedule(self.schedule)

    def add_time(self, time: Union[int, str]):
        time = is_time(time)
        self.schedule.add(time)

    def remove_time(self, time: Union[int, str]):
        time = is_time(time)
        self.schedule.discard(time)


@dataclass
class TimeSlot:
    time: int
    trains: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.time = is_time(self.time)
        self.trains = is_trains(self.trains)

    def add_train(self, train_id: str):
        train_id = is_train_id(train_id)
        self.trains.add(train_id)

    def remove_train(self, train_id: str):
        train_id = is_train_id(train_id)
        self.trains.discard(train_id)
