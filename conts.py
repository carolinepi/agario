from enum import Enum

PORT = 5555
HOST = '127.0.1.1'

WIDTH, HEIGHT = 1600, 830
PLAYER_RADIUS = 10
START_VEL = 9
BALL_RADIUS = 5


class Color(Enum):
    RED = (250, 0, 0)
    YELLOW = (250, 250, 0)
    ORANGE = (200, 100, 50)
    WHITE = (250, 250, 250)


class COMMANDS(Enum):
    move = 'move'
    jump = 'jump'
    get = 'get'
    id = 'id'
