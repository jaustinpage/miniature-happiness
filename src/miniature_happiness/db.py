from typing import Any, KeysView

from sqlitedict import SqliteDict  # type: ignore


class Database:
    def __init__(self) -> None:
        self.d = SqliteDict()

    def get(self, key: str) -> Any:
        """Implement a function to return a value given a key

        :param key: the key to get
        :return: value stored by key
        """
        return self.d.get(key)

    def set(self, key: str, value: Any) -> None:  # noqa: A003
        """Implement a function to store a value for a key

        :param key: The key to set
        :param value: The value to set the key to
        """
        self.d[key] = value
        self.d.commit()

    def keys(self) -> KeysView[str]:
        """Implement a function to return database keys

        :return: keys from the database
        """
        return self.d.keys()
