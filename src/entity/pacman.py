from . import Character
from ..maze import Maze, Direction
import pygame


class Pacman(Character):
    """The player-controlled character navigating the maze."""

    def __init__(self, maze: Maze, super_pacgum_cooldown: int) -> None:
        """Initialize Pac-Man's direction, sprites, and invincibility state.

        Args:
            maze: The maze Pac-Man moves within.
            super_pacgum_cooldown: Duration of the super pacgum effect.
        """
        super().__init__(maze, super_pacgum_cooldown, state_of_sprite=1)
        self._last_move_direction: Direction
        self.reset_last_move_direction()
        self.direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

        self.invincible: bool = False

        self.sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
              "png/entities_sprite.png", 851, 4 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 154 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 304 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 454 + (i * 50), 35, 35)
              for i in range(0, 3, 1)]]

        self.pacman_dying_sprites: list[pygame.Surface] = \
            [self.get_sprite(
             "png/entities_sprite.png", 351, 4 + (i * 50), 35, 35)
             for i in range(0, 11, 1)]

    def _set_starting_position(self) -> tuple[int, int]:
        """Find Pac-Man's starting position, at the maze's center if possible.

        Returns:
            The (line, column) starting position.
        """
        line_pos = (len(self.maze.cases) - 1) // 2
        column_pos = (len(self.maze.cases[0]) - 1) // 2

        if self.verif_position(line_pos, column_pos):
            return (line_pos, column_pos)

        i = 1
        while True:
            j = 0
            while j < i:
                if self.verif_position(line_pos-i + j, column_pos-i):
                    return (line_pos-i + j, column_pos-i)
                if self.verif_position(line_pos-i, column_pos-i + j):
                    return (line_pos-i, column_pos-i + j)
                if self.verif_position(line_pos+i + j, column_pos-i):
                    return (line_pos+i + j, column_pos-i)
                if self.verif_position(line_pos+i, column_pos-i + j):
                    return (line_pos+i, column_pos-i + j)
                j += 1
            i += 1

    def verif_position(self, line_pos: int, column_pos: int) -> bool:
        """Check if a case is not enclosed, and set it as the position if so.

        Args:
            line_pos: Line position to check.
            column_pos: Column position to check.

        Returns:
            True if the position is valid and was set, False otherwise.
        """
        if self.maze.cases[line_pos][column_pos].is_enclosed is False:
            self.line_pos = line_pos
            self.column_pos = column_pos
            return True
        return False

    @property
    def last_move_direction(self) -> Direction:
        """Return the last direction Pac-Man moved in.

        Returns:
            The last move direction.
        """
        return self._last_move_direction

    def reset_last_move_direction(self) -> None:
        """Reset the last move direction to North."""
        self._last_move_direction = Direction.N

    def update_state_of_sprite(self) -> None:
        """Advance Pac-Man's animation frame, cycling between three frames."""
        self.state_of_sprite += 1
        self.state_of_sprite %= 3

    def get_moving_sprite(self) -> pygame.Surface:
        """Return Pac-Man's sprite for its current direction and animation frame.

        Returns:
            The sprite surface to display.
        """
        sprite = self.sprites[self.direction][self.state_of_sprite]
        return sprite

    def move(self, direction: Direction | None) -> None:
        """Move Pac-Man one case in its current facing direction.

        Args:
            direction: Unused; movement follows the current facing direction.
        """
        self.prev_line_pos = self.line_pos
        self.prev_column_pos = self.column_pos
        if self.direction == Character.FacingDirection.UP:
            self.go_up()
        elif self.direction == Character.FacingDirection.RIGHT:
            self.go_right()
        elif self.direction == Character.FacingDirection.DOWN:
            self.go_down()
        elif self.direction == Character.FacingDirection.LEFT:
            self.go_left()
        self.prev_direction = self.direction