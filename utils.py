import math
import random
from typing import Union

from conts import Color


def get_random_color():
    colors = [i for i in Color if i != Color.WHITE]
    return random.choice(colors)


def get_distance(
    position_x1: int,
    position_x2: int,
    position_y1: int,
    position_y2: int,
) -> float:
    return math.sqrt(
        (position_x1 - position_x2) ** 2 + (position_y1 - position_y2) ** 2
    )


def convert_time(t: Union[str, int]) -> str:
    if type(t) == str:
        return t

    if int(t) < 60:
        return str(t) + 's'
    else:
        minutes = str(t // 60)
        seconds = str(t % 60)

        if int(seconds) < 10:
            seconds = '0' + seconds

        return minutes + ':' + seconds
