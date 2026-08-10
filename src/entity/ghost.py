from .entity import Entity
from ..maze import Maze


class Ghost(Entity):

    def __init__(self, line: int, column: int, maze: Maze,
                 super_pacgum_cooldown: int) -> None:
        super().__init__(line, column, maze, super_pacgum_cooldown)
