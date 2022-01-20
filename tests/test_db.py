import pytest
from db import Database


def test_storage():
    """ Asserts that a value can be stored and retrieved from your database """
    d = Database()
    k, v = "A", "1"
    d.set(k, v)
    assert v == d.get(k)


def test_keys():
    """ Asserts that a keys() call to your database returns a key set """
    d = Database()
    data = {"A": "1",
            "B": object,
            "C": 3}

    for k, v in data.items():
        d.set(k, v)
    assert data.keys() == d.keys()

# Implement any other necessary tests
