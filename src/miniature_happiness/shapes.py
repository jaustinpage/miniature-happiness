from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Set, Union


def is_time(time: Union[int, str]) -> int:
    """Check if integer is in the format of HHMM.

    :param time: The time to check. strings are cast to int
    :returns: The time, cast to integer if it was a string
    :raises ValueError: if the time is not valid
    """
    time = int(time)

    if not 0 <= time < 2400:
        raise ValueError("hours must be between 0 and 24")

    if not 0 <= time % 100 < 60:
        raise ValueError("minutes must be between 0 and 60")

    return time


def is_schedule(schedule: Iterable[Union[int, str]]) -> Set[int]:
    """Check if a schedule is valid.

    :param schedule: The schedule to check. Ensures all items in schedule are
        times.
    :returns: The schedule, with times cast to integers.
    """
    schedule = schedule or set()
    schedule_set = {is_time(t) for t in schedule}
    schedule_set.discard(None)  # type: ignore
    return schedule_set or set()


def is_train_id(train_id: str) -> str:
    """Check if a string is a valid train id.

    :param train_id: The train id to check.
    :returns: The train id if it is valid.
    :raises ValueError: If the train id is not valid
    """
    if not isinstance(train_id, str):
        raise ValueError("Must provide train_id as a string")

    if not train_id.isalnum():
        raise ValueError("train id must be alphanumeric")

    if not 0 < len(train_id) <= 4:
        raise ValueError("train id must be 1 to 4 characters long")

    return train_id


def is_trains(trains: Iterable[str]) -> Set[str]:
    """Check if a list of trains are trains.

    :param trains: The trains list to check.
    :returns: The set of trains.
    """
    trains = trains or set()
    trains_set = {is_train_id(t) for t in trains}
    trains_set.discard(None)  # type: ignore
    return trains_set or set()


@dataclass
class TrainSchedule:
    """A schedule of times when a train will be in the station."""

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
    """A time slot in the day."""

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
