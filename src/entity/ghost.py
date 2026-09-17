from .pacman import Pacman
from . import Character
from ..algorithm.dfs import DepthFirstSearch
import random
from ..maze import Maze, Direction
from abc import ABC, abstractmethod
import pygame
import time


class Ghost(Character, ABC):
    """Abstract base class for ghost enemies chasing or fleeing Pac-Man."""

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        """Initialize a ghost's pathfinding, state, and sprites.

        Args:
            maze: The maze the ghost moves within.
            pacman: The Pac-Man instance the ghost interacts with.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            algorithm: Pathfinding algorithm used to reach the ghost's goal.
        """
        super().__init__(maze, super_pacgum_cooldown, state_of_sprite=0)
        self.pacman: Pacman = pacman
        self.freeze: bool = False
        self.algorithm: DepthFirstSearch = algorithm
        self._shortest_path_to_goal: list[tuple[int, int]] | None = None
        self.sprites: list[list[pygame.Surface]]
        self.direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT
        self.death_timer: float | None = None

        self.running_away_sprites: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 1, 554 + (i * 50),
                            35, 35)
            for i in range(0, 2, 1)]
        self.running_away_sprites.extend(
            [self.get_sprite("png/entities_sprite.png", 51, 554 + (i * 50),
                             35, 35)
             for i in range(0, 2, 1)])

    @abstractmethod
    def get_goal(self) -> tuple[int, int]:
        """Decide the ghost's goal position, whether chasing or fleeing.

        Returns:
            The (line, column) position the ghost should path toward.
        """
        ...

    def change_exit_position(self, new_goal: tuple[int, int]) -> None:
        """Update the pathfinding algorithm's exit position.

        Args:
            new_goal: The new (line, column) exit position.
        """
        self.algorithm.set_exit(new_goal)

    def change_entry_position(self) -> None:
        """Update the pathfinding algorithm's entry position to the ghost's current position."""
        self.algorithm.set_entry((self.line_pos, self.column_pos))

    def find_shortest_path_to_exit(self) -> None:
        """Compute and store the shortest path to the current goal."""
        self._shortest_path_to_goal = self.algorithm.solver()

    def do_turn(self) -> None:
        """Compute the ghost's path to its goal and move one step along it."""
        if self.pacman.get_coord() == self.get_coord():
            self.prev_line_pos = self.line_pos
            self.prev_column_pos = self.column_pos
            return
        self.algorithm.set_entry(self.get_coord())
        self.algorithm.set_exit(self.get_goal())
        self.find_shortest_path_to_exit()
        if self.shortest_path_to_goal is None:
            raise ValueError("shortest_path_to_goal cannot be None in"
                             "ghost.do_turn")
        if len(self.shortest_path_to_goal) < 2:
            self.prev_line_pos = self.line_pos
            self.prev_column_pos = self.column_pos
            return
        direction =\
            self.maze.get_direction_between_case(
                self.maze.get_case(self.get_coord()),
                self.maze.get_case(self.shortest_path_to_goal[1])
                )
        if direction is None:
            raise ValueError("direction cannot be None in ghost.do_turn")
        self.move(direction)

    @property
    def shortest_path_to_goal(self) -> list[tuple[int, int]] | None:
        """Return the cached shortest path to the ghost's goal.

        Returns:
            The list of (line, column) positions forming the path.

        Raises:
            ValueError: If no path has been computed yet.
        """
        if self._shortest_path_to_goal is None:
            raise ValueError(
                f"{type(self).__name__} doesn't have a path to its goal")

        return self._shortest_path_to_goal

    def run_away(self) -> tuple[int, int]:
        """Get the maze corner furthest from Pac-Man's current position.

        Returns:
            The (line, column) position of the furthest corner.
        """
        if self.pacman.line_pos <= len(self.maze.cases) // 2:
            if self.pacman.column_pos <= len(self.maze.cases[0]) // 2:
                return (self.maze.nb_line - 1, self.maze.nb_column - 1)
            else:
                return (self.maze.nb_line - 1, 0)
        else:
            if self.pacman.column_pos <= len(self.maze.cases[0]) // 2:
                return (0, self.maze.nb_column - 1)
            else:
                return (0, 0)

    def chase_pacman(self) -> tuple[int, int]:
        """Get Pac-Man's current position as a chase target.

        Returns:
            Pac-Man's (line, column) position.
        """
        return (self.pacman.line_pos, self.pacman.column_pos)

    def get_chasing_sprite(self) -> pygame.Surface:
        """Return the ghost's sprite for its current direction and animation frame.

        Returns:
            The sprite surface to display while hunting.
        """
        sprite = self.sprites[self.direction][self.state_of_sprite]
        return sprite

    def update_state_of_sprite(self) -> None:
        """Advance the ghost's animation frame, cycling between two frames."""
        self.state_of_sprite += 1
        self.state_of_sprite %= 2

    def get_fleeing_sprite(self) -> pygame.Surface:
        """Return the ghost's sprite while fleeing, flashing near cooldown end.

        Returns:
            The sprite surface to display while running away.
        """
        if self.super_pacgum_cooldown is not None and\
                self.super_pacgum_cooldown - time.monotonic() < 3:
            return self.running_away_sprites[self.state_of_sprite + 2]
        return self.running_away_sprites[self.state_of_sprite]

    def get_valid_sprite(self) -> pygame.Surface:
        """Return the appropriate sprite based on the ghost's current state.

        Returns:
            The sprite surface to display.
        """
        if self.state == self.State.HUNTING:
            return self.get_chasing_sprite()
        else:
            return self.get_fleeing_sprite()

    def die(self) -> None:
        """Kill the ghost, starting its respawn timer and resetting its position."""
        self.death_timer = 5
        self.reset_starting_position()


class Shadow(Ghost):  # red chase
    """Red ghost that directly chases or flees from Pac-Man."""

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        """Initialize Shadow's starting position and sprites.

        Args:
            maze: The maze the ghost moves within.
            pacman: The Pac-Man instance the ghost interacts with.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            algorithm: Pathfinding algorithm used to reach the ghost's goal.
        """
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.sprites = \
            [[self.get_sprite(
             "png/entities_sprite.png", 1, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Return the corner to flee to when running, or Pac-Man's position when hunting.

        Returns:
            The (line, column) goal position.
        """
        if self.state == Character.State.RUNNING:
            return self.run_away()

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        """Return Shadow's starting (line, column) position in the maze.

        Returns:
            The top-left corner of the maze.
        """
        return (0, 0)


class Speedy(Ghost):  # pink flank
    """Pink ghost that ambushes Pac-Man ahead of its movement direction."""

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        """Initialize Speedy's starting position and sprites.

        Args:
            maze: The maze the ghost moves within.
            pacman: The Pac-Man instance the ghost interacts with.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            algorithm: Pathfinding algorithm used to reach the ghost's goal.
        """
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.sprites = \
            [[self.get_sprite(
              "png/entities_sprite.png", 51, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Return a position ahead of Pac-Man to ambush it, or a flee corner.

        Returns:
            The (line, column) goal position.
        """
        if self.state == Character.State.RUNNING:
            return self.run_away()

        for cardinal_point in Direction:
            if self.pacman.last_move_direction == cardinal_point:
                for i in range(3, 0, -1):
                    new_line_pos = \
                        self.pacman.line_pos + cardinal_point.value[0] * i
                    new_column_pos = \
                        self.pacman.column_pos + cardinal_point.value[1] * i

                    if self.maze.is_accessible(new_line_pos, new_column_pos):
                        return (new_line_pos, new_column_pos)

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        """Return Speedy's starting (line, column) position in the maze.

        Returns:
            The top-right corner of the maze.
        """
        return (0, self.maze.nb_column - 1)


class Bashful(Ghost):  # cyan random
    """Cyan ghost that wanders to random accessible positions."""

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        """Initialize Bashful's starting position and sprites.

        Args:
            maze: The maze the ghost moves within.
            pacman: The Pac-Man instance the ghost interacts with.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            algorithm: Pathfinding algorithm used to reach the ghost's goal.
        """
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.sprites = \
            [[self.get_sprite(
              "png/entities_sprite.png", 101, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Return a random accessible position, or a flee corner when running.

        Returns:
            The (line, column) goal position.
        """
        if self.state == Character.State.RUNNING:
            return self.run_away()

        new_line = -1
        new_column = -1

        while not self.maze.is_accessible(new_line, new_column):
            new_line = random.randint(0, self.maze.nb_line - 1)
            new_column = random.randint(0, self.maze.nb_column - 1)
        return (new_line, new_column)

    def _set_starting_position(self) -> tuple[int, int]:
        """Return Bashful's starting (line, column) position in the maze.

        Returns:
            The bottom-left corner of the maze.
        """
        return (self.maze.nb_line - 1, 0)


class Pokey(Ghost):  # orange chase + run away
    """Orange ghost that chases Pac-Man but flees when too close."""

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        """Initialize Pokey's starting position and sprites.

        Args:
            maze: The maze the ghost moves within.
            pacman: The Pac-Man instance the ghost interacts with.
            super_pacgum_cooldown: Duration of the super pacgum effect.
            algorithm: Pathfinding algorithm used to reach the ghost's goal.
        """
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.sprites = \
            [[self.get_sprite(
              "png/entities_sprite.png", 151, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Return a flee corner when running or too close, otherwise chase Pac-Man.

        Returns:
            The (line, column) goal position.
        """
        if self.state == Character.State.RUNNING or self.is_pacman_too_close():
            return self.run_away()
        else:
            return self.chase_pacman()

    def is_pacman_too_close(self) -> bool:
        """Check whether Pac-Man is within a 3-case range of this ghost.

        Returns:
            True if Pac-Man is too close, False otherwise.
        """
        if (self.line_pos - self.pacman.line_pos < 3 and
           self.line_pos - self.pacman.line_pos > -3):
            if (self.column_pos - self.pacman.column_pos < 3 and
               self.column_pos - self.pacman.column_pos > -3):
                return True
        return False

    def _set_starting_position(self) -> tuple[int, int]:
        """Return Pokey's starting (line, column) position in the maze.

        Returns:
            The bottom-right corner of the maze.
        """
        return (self.maze.nb_line - 1, self.maze.nb_column - 1)