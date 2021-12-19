from models.position import Position


class Player:

    def __init__(self, id: int, position: Position, name: str):
        self._id = id
        self._position = position
        self.color = (255, 128, 0)   # TODO: choose color
        self.score = 0
        self.name = name

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
    def position(self, position: Position):
        self._position = position
