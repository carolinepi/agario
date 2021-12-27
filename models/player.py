from typing import Optional

from conts import Color
from models.player_addition import PlayerAddition
from models.position import Position
from utils import get_distance


class Player:
    START_RADIUS = 8

    def __init__(
        self,
        id: int,
        position: Position,
        name: str,
        color: Color
    ):
        self._id = id
        self._position = position
        self.color = color
        self.score = 0
        self.name = name
        self.addition = []

    @property
    def x(self) -> int:
        return self.x

    @property
    def y(self) -> int:
        return self.y

    def recreate(self, position: Position) -> None:
        self.score = 0
        self.position = position

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position) -> None:
        self._position = position
        self.regenerate_player_addition()

    def regenerate_player_addition(self) -> None:
        for i, add in enumerate(self.addition):
            dis = get_distance(
                self.position.x, add.position.x,
                self.position.y, add.position.y,
            )
            if dis < (self.START_RADIUS + self.score) * 0.65:
                self.addition.clear()
                return

            player_addition = self._generate_player_addition(
                add.direction, add.temp
            )
            self.addition[i] = player_addition

    def generate_player_addition(self, direction: str) -> None:
        loaded_directions = [add.direction for add in self.addition]
        if direction in loaded_directions:
            return

        player_addition = self._generate_player_addition(direction)
        self.addition.append(player_addition)

    def _generate_player_addition(
        self,
        direction: str,
        temp: Optional[int] = None,
    ) -> PlayerAddition:
        temp = int(self.score - (self.score / 20)) if temp is None else temp
        x = self.position.x
        y = self.position.y
        if direction == 'up':
            y = self.position.y - self.START_RADIUS - temp
        if direction == 'down':
            y = self.position.y + self.START_RADIUS + temp
        if direction == 'right':
            x = self.position.x + self.START_RADIUS + temp
        if direction == 'left':
            x = self.position.x - self.START_RADIUS - temp
        return PlayerAddition(Position(x, y), direction, temp)

