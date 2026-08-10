from entity import Entity
from ..maze import Maze


class Ghost(Entity):

    def __init__(self, line: int, column: int, maze: Maze) -> None:
        super().__init__(line, column)
