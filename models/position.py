from dataclasses import dataclass


@dataclass
class Position:
    __slots__ = 'x', 'y'

    x: int
    y: int
