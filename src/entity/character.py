from ..maze import Maze, Direction
from enum import IntEnum
from abc import abstractmethod, ABC
from . import Entity


class Character(Entity, ABC):

    class Direction(IntEnum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

    class State(Enum):
        HUNTING = 0
        RUNNING = 1

    def __init__(self, maze: Maze, super_pacgum_cooldown: int) -> None:

        super().__init__()
        self.maze: Maze = maze
        self.starting_position: tuple[int, int] = self._set_starting_position()
        self.line_pos: int = self.starting_position[0]
        self.column_pos: int = self.starting_position[1]
        self.super_pacgum_cooldown: int = super_pacgum_cooldown
        self.state: Character.State = self.State.RUNNING
        self.direction: Character.Direction = self.Direction.RIGHT

    def go_left(self) -> None:
        """Go one case left in the maze"""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.W):
            self.column_pos -= 1

    def go_right(self) -> None:
        """Go one case right in the maze"""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.E):
            self.column_pos += 1

    def go_up(self) -> None:
        """Go one case up in the maze"""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.N):
            self.line_pos -= 1

    def go_down(self) -> None:
        """Go one case down in the maze"""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.S):
            self.line_pos += 1

    def move(self, direction: Direction) -> None:
        if direction == Direction.N:
            self.go_up()
        elif direction == Direction.E:
            self.go_right()
        elif direction == Direction.S:
            self.go_down()
        else:
            self.go_left()

    def change_state(self) -> None:
        """Alternate the state between hunting and running for entities"""
        if self.state == self.State.HUNTING:
            self.state = self.State.RUNNING
        else:
            self.state = self.State.HUNTING

    def reset_super_pacgum_cooldown(self) -> None:
        """Reset the timer of the super pacgum effect"""
        self.super_pacgum_cooldown = self.super_pacgum_cooldown

    @abstractmethod
    def _set_starting_position(self) -> tuple[int, int]: ...
