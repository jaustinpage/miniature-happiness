from collections import deque
from typing import List

from miniature_happiness.db import Database
from miniature_happiness.shapes import TimeSlot, TrainSchedule, is_time

d = Database()


def get_train_schedule(train_id: str) -> TrainSchedule:
    schedule = d.get("train_id:" + train_id, set())
    return TrainSchedule(id=train_id, schedule=schedule)


def save_train_schedule(train_schedule: TrainSchedule) -> None:
    d.set("train_id:" + train_schedule.id, train_schedule.schedule)


def list_train_schedules() -> List[str]:
    return [x.split(":", 1)[1] for x in d.keys() if x.startswith("train_id:")]


def get_time_slot(time: int) -> TimeSlot:
    trains = d.get("time:" + str(time), set())
    return TimeSlot(time=time, trains=trains)


def save_time_slot(time_slot: TimeSlot) -> None:
    d.set("time:" + str(time_slot.time), time_slot.trains)


def list_time_slots() -> list[int]:
    return [int(x.split(":", 1)[1]) for x in d.keys() if x.startswith("time:")]


def update_train_schedule(train_schedule: TrainSchedule) -> None:
    old_train_schedule = get_train_schedule(train_schedule.id)
    time_slot_deletions = old_train_schedule.schedule.difference(
        train_schedule.schedule
    )
    time_slot_additions = train_schedule.schedule.difference(
        old_train_schedule.schedule
    )

    for time_slot in time_slot_deletions:
        time_slot = get_time_slot(time_slot)
        time_slot.trains.discard(train_schedule.id)
        save_time_slot(time_slot)

    for time_slot in time_slot_additions:
        time_slot = get_time_slot(time_slot)
        time_slot.trains.add(train_schedule.id)
        save_time_slot(time_slot)

    save_train_schedule(train_schedule)


def update_time_slot(time_slot: TimeSlot) -> None:
    old_time_slot = get_time_slot(time_slot.time)
    train_schedule_deletions = old_time_slot.trains.difference(time_slot.trains)
    train_schedule_additions = time_slot.trains.difference(old_time_slot.trains)

    for train_schedule in train_schedule_deletions:
        train_schedule = get_train_schedule(train_schedule)
        train_schedule.schedule.discard(time_slot.time)
        save_train_schedule(train_schedule)

    for train_schedule in train_schedule_additions:
        train_schedule = get_train_schedule(train_schedule)
        train_schedule.schedule.add(time_slot.time)
        save_train_schedule(train_schedule)

    save_time_slot(time_slot)



def get_next_conflict(start_time: int = 1, number_of_trains: int = 2) -> int:
    start_time = is_time(start_time)

    # max number of time slots is 24hr * 60min
    time_slots = sorted(list_time_slots())

    # rotate the list to start at the first time after the indicated time.
    index = 0
    for i, time in enumerate(time_slots):
        if time >= start_time:
            index = i
            break

    time_slots = deque(time_slots)
    time_slots.rotate(index)
    time_slots = list(time_slots)

    for time in time_slots:
        if len(get_time_slot(time).trains) >= number_of_trains:
            return time
