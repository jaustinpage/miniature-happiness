from app import app
import json
import pytest
import requests

# You are welcome to use a Flask client fixture or test the running instance, as below
BASE_URL = 'http://127.0.0.1:5000/'


def test_startup():
    """Asserts that your service starts and responds"""
    r = requests.get(BASE_URL)
    assert r.status_code == 200 and r.text == "OK"


@pytest.mark.parametrize("train", [
    {'id': 'TOMO', 'schedule': [180, 640, 1440]},
    {'id': 'FOMO', 'schedule': [440, 640]},
    {'id': '1', 'schedule': [100, 220, 300]}
])
def test_add(train):
    """Asserts that schedules are added and returned as expected"""

    requests.post(f"{BASE_URL}/trains", json=train)
    r = requests.get(f"{BASE_URL}/trains/{train['id']}")

    assert r.json() == train['schedule']


def test_next():
    """ Implement a test for the /trains/next functionality"""
    raise NotImplementedError


# Implement any other necessary tests
