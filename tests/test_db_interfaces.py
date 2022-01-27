import pytest

import miniature_happiness.db_interfaces
from miniature_happiness.db import Database
from miniature_happiness.db_interfaces import (
    get_next_conflict,
    get_time_slot,
    get_train_schedule,
    list_time_slots,
    list_train_schedules,
    save_time_slot,
    save_train_schedule,
    update_time_slot,
    update_train_schedule,
)
from miniature_happiness.shapes import TimeSlot, TrainSchedule


@pytest.fixture()
def _new_db(monkeypatch):
    monkeypatch.setattr(miniature_happiness.db_interfaces, "d", Database())


@pytest.mark.usefixtures("_new_db")
def test_train_schedule():
    save_train_schedule(TrainSchedule("abc", [1, 2100]))
    schedule = get_train_schedule("abc")
    assert schedule.id == "abc"
    assert schedule.schedule == {1, 2100}
    assert ["abc"] == list_train_schedules()


@pytest.mark.usefixtures("_new_db")
def test_time_slot():
    save_time_slot(TimeSlot(1, ["abc", "def"]))
    time_slot = get_time_slot(1)
    assert time_slot.time == 1
    assert time_slot.trains == {"abc", "def"}
    assert [1] == list_time_slots()


@pytest.mark.usefixtures("_new_db")
def test_update_train_schedule():
    update_train_schedule(TrainSchedule("abc", [1, 2100]))
    assert get_train_schedule("abc").schedule == {1, 2100}
    update_train_schedule(TrainSchedule("abc", [2100, 2300]))
    assert get_train_schedule("abc").schedule == {2100, 2300}
    update_train_schedule(TrainSchedule("abc", [2100]))
    assert get_train_schedule("abc").schedule == {2100}


@pytest.mark.usefixtures("_new_db")
def test_update_time_slot():
    update_time_slot(TimeSlot(1, ["abc", "def"]))
    assert get_time_slot(1).trains == {"abc", "def"}
    update_time_slot(TimeSlot(1, ["abc", "123"]))
    assert get_time_slot(1).trains == {"abc", "123"}
    update_time_slot(TimeSlot(1, ["123"]))
    assert get_time_slot(1).trains == {"123"}


@pytest.mark.usefixtures("_new_db")
def test_next_conflict():
    assert get_next_conflict() is None
    update_time_slot(TimeSlot(2359, ["abc", "def"]))
    assert get_next_conflict() == 2359
    update_time_slot(TimeSlot(1200, ["abc", "def"]))
    assert get_next_conflict() == 1200
    update_time_slot(TimeSlot(1, ["abc", "def"]))
    assert get_next_conflict() == 1
    assert get_next_conflict(1000) == 1200
    assert get_next_conflict(1300) == 2359
    assert get_next_conflict(number_of_trains=3) is None
    update_time_slot(TimeSlot(1, ["abc", "def", "ghi"]))
    assert get_next_conflict(number_of_trains=3) == 1
    assert get_next_conflict(1000, number_of_trains=3) == 1
    update_time_slot(TimeSlot(1200, ["abc", "def", "ghi"]))
    assert get_next_conflict(1000, number_of_trains=3) == 1200
