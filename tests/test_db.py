from miniature_happiness.db import Database


def test_storage():
    """Asserts that a value can be stored and retrieved from your database"""
    d = Database()
    k, v = "A", "1"
    d.set(k, v)
    assert v == d.get(k)


def test_keys():
    """Asserts that a keys() call to your database returns a key set"""
    d = Database()
    data = {"A": "1", "B": object, "C": 3}

    for k, v in data.items():
        d.set(k, v)
    assert list(data.keys()) == list(d.keys())


# Implement any other necessary tests
def test_null():
    d = Database()
    assert d.get("UNKNOWN") is None


def test_set():
    d = Database()
    data = {"A": {}, "B": {1}, "C": {1, 2, 3}}

    for k, v in data.items():
        d.set(k, v)
        assert d.get(k) == data[k]
    assert list(data.keys()) == list(d.keys())
