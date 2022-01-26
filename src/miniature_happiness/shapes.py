from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from typing import Any, Callable, ClassVar, Dict, Iterable, List, Set, Union, Type

StrInt = Union[str, int]

class Validator(ABC):
    """Descriptor to validate data."""
    def __set_name__(self, owner, name) -> None:
        self.name = f"_{name}"
        
    def __get__(self, instance, owner=None):
        return getattr(instance, self.name)
    
    def __set__(self, instance, value) -> None:
        value = self.validate(value) or value
        setattr(instance, self.name, value)
        
    @abstractmethod
    def validate(self, value):
        pass
    
    
class MinuteOfDay(Validator):
    def validate(self, value: StrInt) -> int:
        time = int(value)
        if not 0 <= time < 2400:
            raise ValueError("hours must be between 0 and 24")

        if not 0 <= time % 100 < 60:
            raise ValueError("minutes must be between 0 and 60")

        return time
    

class TrainID(Validator):
    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Must provide train_id as a string")

        if not value.isalnum():
            raise ValueError("train id must be alphanumeric")

        if not 0 < len(value) <= 4:
            raise ValueError("train id must be 1 to 4 characters long")


class SetOf(Validator):
    def __init__(self, set_type: Type[Validator]) -> None:
        self.set_type = set_type
        
    def validate(self, value: Iterable[StrInt]) -> Set[StrInt]:
        values = value or set()
        values = {self.set_type(i) for i in values}
        values.discard(None)
        return values or set()
    
    
class RegisteredTypes:
    _registry: Dict[str, Callable]
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls
        

class TrainScheduleC(RegisteredTypes):
    key = TrainID()
    collection = SetOf(MinuteOfDay)
    
    
class TimeSlotC(RegisteredTypes):
    key = MinuteOfDay()
    collection = SetOf(TrainID)
    


def is_time(time: StrInt) -> int:
    time = int(time)

    if not 0 <= time < 2400:
        raise ValueError("hours must be between 0 and 24")

    if not 0 <= time % 100 < 60:
        raise ValueError("minutes must be between 0 and 60")

    return time


def is_train_id(train_id: str) -> str:
    if not isinstance(train_id, str):
        raise ValueError("Must provide train_id as a string")

    if not train_id.isalnum():
        raise ValueError("train id must be alphanumeric")

    if not 0 < len(train_id) <= 4:
        raise ValueError("train id must be 1 to 4 characters long")

    return train_id


def _is_set(of: Callable[[StrInt], StrInt], values: Iterable[StrInt]) -> Set[StrInt]:
    values = values or set()
    values = {of(i) for i in values}
    values.discard(None)
    return values or set()


def is_schedule(schedule: Iterable[StrInt]):
    return _is_set(is_time, schedule)


def is_trains(trains: Iterable[StrInt]):
    return _is_set(is_train_id, trains)


_db_types: Dict[str, callable] = {}


def db_dataclass(cls):
    cls = dataclass(cls)

    for a_field in fields(cls):
        if "db_key" in a_field.metadata:

            def key(self):
                return f"{cls.__name__}:{getattr(self, a_field.name)}"

            cls.key = key

        if "db_value" in a_field.metadata:

            def value(self):
                return getattr(self, a_field.name)

            cls.value = value

    #if cls.key and cls.value:
    #    raise ValueError(
    #        "Can only decorate dataclass like classes that provide "
    #        'metadata in fields that includes "db_key" and "db_value"'
    #    )

    _db_types[cls.__name__] = cls

    def to_db(self):
        return self.key, self.value

    cls.to_db = to_db


def get(key: str, value: Any) -> object:
    tag, key = key.split(":", 1)
    return _db_types[tag](key, value)



@dataclass
class TrainSchedule:
    id: str = field(metadata={"db_key": "a_key"})
    schedule: Set[int] = field(default_factory=set, metadata={"db_value": "a_value"})

    def __post_init__(self):
        self.id = is_train_id(self.id)
        self.schedule = is_schedule(self.schedule)

    def add_time(self, time: Union[int, str]):
        time = is_time(time)
        self.schedule.add(time)

    def remove_time(self, time: Union[int, str]):
        time = is_time(time)
        self.schedule.discard(time)


@dataclass
class TimeSlot:
    time: int
    trains: Set[str] = field(default_factory=set)

    def __post_init__(self):
        self.time = is_time(self.time)
        self.trains = is_trains(self.trains)

    def add_train(self, train_id: str):
        train_id = is_train_id(train_id)
        self.trains.add(train_id)

    def remove_train(self, train_id: str):
        train_id = is_train_id(train_id)
        self.trains.discard(train_id)
