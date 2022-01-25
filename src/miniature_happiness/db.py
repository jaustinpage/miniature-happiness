from typing import Any, KeysView

from sqlitedict import SqliteDict


class Database:
    def __init__(self):
        self.d = SqliteDict()

    def get(self, key: str) -> Any:
        """Implement a function to return a value given a key"""
        return self.d.get(key)

    def set(self, key: str, val: Any) -> None:
        """Implement a function to store a value for a key"""
        self.d[key] = val
        self.d.commit()

    def keys(self) -> KeysView[str]:
        """Implement a function to return database keys"""
        return self.d.keys()
