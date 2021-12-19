from dataclasses import dataclass

from models.position import Position
from conts import Color


@dataclass(frozen=True)
class Ball:
    position: Position
    color: Color

