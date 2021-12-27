from models.position import Position


class PlayerAddition:
    def __init__(
        self,
        position: Position,
        direction: str,
        temp: int
    ):
        self._position = position
        self.direction = direction
        self.temp = temp

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position


