import pytest

from miniature_happiness.shapes import TimeSlot, TrainSchedule


def test_train_schedule():
    ts = TrainSchedule(id="ABC")
    assert ts.id == "ABC"
    ts.add_time(1)
    assert ts.schedule == {1}
    ts.add_time(2201)
    assert ts.schedule == {1, 2201}


@pytest.mark.parametrize(
    ("arg", "message"),
    [
        (None, "Must provide train_id as a string"),
        ("ABCDE", "train id must be 1 to 4 characters long"),
    ],
)
def test_train_schedule_validation(arg, message):
    with pytest.raises(ValueError, match=message):
        TrainSchedule(id=arg)


def test_time_slot():
    ts = TimeSlot(time=1)
    assert ts.time == 1
    ts.add_train("ABC")
    assert ts.trains == {"ABC"}
    ts.add_train("DEF")
    assert ts.trains == {"ABC", "DEF"}


@pytest.mark.parametrize(
    ("arg", "message"),
    [
        (-1, "hours must be between 0 and 24"),
        (2400, "hours must be between 0 and 24"),
        (2280, "minutes must be between 0 and 60"),
    ],
)
def test_time_slot_validation(arg, message):
    with pytest.raises(ValueError, match=message):
        TimeSlot(time=arg)
