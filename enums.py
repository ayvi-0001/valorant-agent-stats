import typing as t
from enum import Enum

__all__: t.Sequence[str] = ("Rank", "Episode", "Act")


class Rank(int, Enum):
    radiant = 27
    immortal3 = 26
    immortal2 = 25
    immortal1 = 24
    ascendant3 = 23
    ascendant2 = 22
    ascendant1 = 21
    diamond3 = 20
    diamond2 = 19
    diamond1 = 18
    platinum3 = 17
    platinum2 = 16
    platinum1 = 15
    gold3 = 14
    gold2 = 13
    gold1 = 12
    silver3 = 11
    silver2 = 10
    silver1 = 9
    bronze3 = 8
    bronze2 = 7
    bronze1 = 6
    iron3 = 5
    iron2 = 4
    iron1 = 3


class ValueEnum(Enum):
    def __get__(self, instance: t.Any, owner: t.Any) -> str:
        return self.value


class Episode(str, ValueEnum):
    eight = "e8"
    seven = "e7"
    six = "e6"
    five = "e5"
    four = "e4"
    three = "e3"
    two = "e2"
    one = "e1"


class Act(str, ValueEnum):
    three = "act3"
    two = "act2"
    one = "act1"
