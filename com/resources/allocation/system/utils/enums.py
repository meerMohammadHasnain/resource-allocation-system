from enum import Enum


class StringEnum(Enum):

    @classmethod
    def map(cls):
        return cls._value2member_map_

    @classmethod
    def all_enums(cls):
        return cls.map().values()

    @classmethod
    def all_strings(cls):
        return cls.map().keys()

    @classmethod
    def from_str(cls, value):
        return cls.map().get(value)

    def __str__(self):
        return self.value
