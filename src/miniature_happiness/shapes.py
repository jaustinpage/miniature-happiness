from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Set, Union


def is_time(time: Union[int, str]) -> int:
    time = int(time)

    if not 0 <= time < 2400:
        raise ValueError("hours must be between 0 and 24")

    if not 0 <= time % 100 < 60:
        raise ValueError("minutes must be between 0 and 60")

    return time


def is_schedule(schedule: Iterable[Union[int, str]]) -> Set[int]:
    schedule = schedule or set()
    schedule_set = {is_time(t) for t in schedule}
    schedule_set.discard(None)  # type: ignore
    return schedule_set or set()


def is_train_id(train_id: str) -> str:
    if not isinstance(train_id, str):
        raise ValueError("Must provide train_id as a string")

    if not train_id.isalnum():
        raise ValueError("train id must be alphanumeric")

    if not 0 < len(train_id) <= 4:
        raise ValueError("train id must be 1 to 4 characters long")

    return train_id


def is_trains(trains: Iterable[str]) -> Set[str]:
    trains = trains or set()
    trains_set = {is_train_id(t) for t in trains}
    trains_set.discard(None)  # type: ignore
    return trains_set or set()


@dataclass
class TrainSchedule:
    id: str  # noqa: A003
    schedule: Set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.id = is_train_id(self.id)
        self.schedule = is_schedule(self.schedule)

    def add_time(self, time: Union[int, str]) -> None:
        time = is_time(time)
        self.schedule.add(time)

    def remove_time(self, time: Union[int, str]) -> None:
        time = is_time(time)
        self.schedule.discard(time)


@dataclass
class TimeSlot:
    time: int
    trains: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.time = is_time(self.time)
        self.trains = is_trains(self.trains)

    def add_train(self, train_id: str) -> None:
        train_id = is_train_id(train_id)
        self.trains.add(train_id)

    def remove_train(self, train_id: str) -> None:
        train_id = is_train_id(train_id)
        self.trains.discard(train_id)
