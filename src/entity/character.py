from ..maze import Maze, Direction
from enum import Enum, IntEnum
from abc import abstractmethod, ABC
from . import Entity


class Character(Entity, ABC):
    """Abstract base class for maze characters (Pac-Man and ghosts)."""

    class FacingDirection(IntEnum):
        """Direction a character sprite is currently facing."""

        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

    class State(Enum):
        """Behavioral state of a character."""

        HUNTING = 0
        RUNNING = 1

    def __init__(self, maze: Maze, super_pacgum_cooldown: int,
                 state_of_sprite: int) -> None:
        """Initialize a character's position, state, and sprite direction.

        Args:
            maze: The maze the character moves within.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            state_of_sprite: Initial sprite state index.
        """
        super().__init__()
        self.maze: Maze = maze
        self.starting_position: tuple[int, int] = self._set_starting_position()
        self.line_pos: int = self.starting_position[0]
        self.column_pos: int = self.starting_position[1]
        self.prev_line_pos: int = self.line_pos
        self.prev_column_pos: int = self.column_pos
        self.super_pacgum_cooldown: float | None = super_pacgum_cooldown
        self.state: Character.State = self.State.HUNTING
        self.direction: Character.FacingDirection = self.FacingDirection.RIGHT
        self.state_of_sprite: int = state_of_sprite
        self.prev_direction: Character.FacingDirection = self.direction

    def go_left(self) -> None:
        """Move one case left in the maze, if travelable."""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.W):
            self.column_pos -= 1

    def go_right(self) -> None:
        """Move one case right in the maze, if travelable."""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.E):
            self.column_pos += 1

    def go_up(self) -> None:
        """Move one case up in the maze, if travelable."""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.N):
            self.line_pos -= 1

    def go_down(self) -> None:
        """Move one case down in the maze, if travelable."""
        if self.maze.is_travelable(
           self.maze.cases[self.line_pos][self.column_pos], Direction.S):
            self.line_pos += 1

    def move(self, direction: Direction | None) -> None:
        """Move the character one case in the given direction.

        Args:
            direction: The direction to move in, or None to stay in place.
        """
        self.prev_line_pos = self.line_pos
        self.prev_column_pos = self.column_pos
        if direction == Direction.N:
            self.go_up()
            self.direction = self.FacingDirection.UP
        elif direction == Direction.E:
            self.go_right()
            self.direction = self.FacingDirection.RIGHT
        elif direction == Direction.S:
            self.go_down()
            self.direction = self.FacingDirection.DOWN
        elif direction == Direction.W:
            self.go_left()
            self.direction = self.FacingDirection.LEFT
        self.prev_direction = self.direction

    def change_state(self) -> None:
        """Toggle the character's state between hunting and running."""
        if self.state == self.State.HUNTING:
            self.state = self.State.RUNNING
        else:
            self.state = self.State.HUNTING

    def reset_super_pacgum_cooldown(self) -> None:
        """Reset the timer of the super pacgum effect."""
        self.super_pacgum_cooldown = self.super_pacgum_cooldown

    def reset_starting_position(self) -> None:
        """Reset the character's position to its starting position."""
        self.line_pos, self.column_pos = self.starting_position
        self.prev_line_pos = self.line_pos
        self.prev_column_pos = self.column_pos

    @abstractmethod
    def update_state_of_sprite(self) -> None:
        """Update the sprite state index based on the character's status."""
        ...

    @abstractmethod
    def _set_starting_position(self) -> tuple[int, int]:
        """Return the character's starting (line, column) position in the maze."""
        ...