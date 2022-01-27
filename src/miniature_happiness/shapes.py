from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterable, Iterator, MutableSet
from dataclasses import dataclass, field
from typing import Any, Optional, Set, Type, Union

StrInt = Union[str, int]


class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(value: Any) -> Any:
        """The validator to use to validate a value.

        :param value: The value to validate
        :returns: A cast and coerced value.
        """
        pass  # pragma: no cover

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any) -> None:
        value = self.validate(value)
        setattr(obj, self.private_name, value)


class HoursMinutes(Validator):
    """Validator to ensure int of HHMM."""

    @staticmethod
    def validate(value: StrInt) -> int:
        """Check if integer is in the format of HHMM.

        :param value: The time to check. strings are cast to int
        :returns: The time, cast to integer if it was a string
        :raises ValueError: if the time is not valid
        """
        time = int(value)
        if not 0 <= time < 2400:
            raise ValueError("hours must be between 0 and 24")

        if not 0 <= time % 100 < 60:
            raise ValueError("minutes must be between 0 and 60")
        return time


class TrainID(Validator):
    """Validator to ensure train id."""

    @staticmethod
    def validate(value: str) -> str:
        """Check if a string is a valid train id.

        :param value: The train id to check.
        :returns: The train id if it is valid.
        :raises ValueError: If the train id is not valid
        """
        if not isinstance(value, str):
            raise ValueError("Must provide train_id as a string")

        if not value.isalnum():
            raise ValueError("train id must be alphanumeric")

        if not 0 < len(value) <= 4:
            raise ValueError("train id must be 1 to 4 characters long")

        return value


class ValidatorSet(MutableSet):
    """A set that validates the elements of the set."""

    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        iterable = iterable or set()
        self.elements = {self._validator.validate(i) for i in iterable}
        self.elements.discard(None)  # type: ignore

    @property
    @abstractmethod
    def _validator(self) -> Type[Validator]:
        """The validator to use for elements of the set."""

    def add(self, value: Hashable) -> None:
        self.elements.add(self._validator.validate(value))

    def discard(self, value: Hashable) -> None:
        self.elements.discard(value)

    def __iter__(self) -> Iterator:
        return iter(self.elements)

    def __contains__(self, value: Hashable) -> bool:
        return value in self.elements

    def __len__(self) -> int:
        return len(self.elements)


class ScheduleSet(ValidatorSet):
    _validator = HoursMinutes


class TrainsSet(ValidatorSet):
    _validator = TrainID


class ScheduleValidator(Validator):
    @staticmethod
    def validate(value: Union["ScheduleValidator", Iterable]) -> ScheduleSet:
        if isinstance(value, Iterable):
            return ScheduleSet(value)
        return ScheduleSet(None)


class TrainsValidator(Validator):
    @staticmethod
    def validate(value: Union["TrainsValidator", Iterable]) -> TrainsSet:
        if isinstance(value, Iterable):
            return TrainsSet(value)
        return TrainsSet(None)


@dataclass
class TrainSchedule:
    """A schedule of times when a train will be in the station."""

    id: Union[str, TrainID] = field(default=TrainID())  # noqa: A003
    schedule: Union[Set[int], ScheduleValidator] = field(default=ScheduleValidator())


@dataclass
class TimeSlot:
    """A time slot in the day."""

    time: Union[int, HoursMinutes] = field(default=HoursMinutes())
    trains: Union[Set[str], TrainsValidator] = field(default=TrainsValidator())
