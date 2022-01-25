import pytest

trains = [
    {"id": "TOMO", "schedule": [140, 640, 1440]},
    {"id": "FOMO", "schedule": [440, 640]},
    {"id": "1", "schedule": [100, 220, 300]},
]


def test_startup(client):
    """Asserts that your service starts and responds"""
    r = client.get("/")
    assert r.status_code == 200
    assert r.data == b"OK"


@pytest.mark.parametrize("train", trains)
def test_add(train, client):
    """Asserts that schedules are added and returned as expected"""

    client.post("/trains", json=train)
    r = client.get(f"/trains/{train['id']}")

    assert sorted(r.json) == sorted(train["schedule"])


def test_next(client):
    """Implement a test for the /trains/next functionality"""  # noqa: DAR401
    for train in trains:
        client.post("/trains", json=train)
    r = client.get("/trains/next")
    assert r.data == b"640"


# Implement any other necessary tests
