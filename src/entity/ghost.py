from .pacman import Pacman
from . import Character
from ..algorithm.dfs import DepthFirstSearch
import random
from ..maze import Maze, Direction
from abc import ABC


class Ghost(Character, ABC):

    def __init__(self, maze: Maze, starting_position: tuple[int, int],
                 pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch
                 ) -> None:
        super().__init__(maze, super_pacgum_cooldown)
        self.starting_position: tuple[int, int] = starting_position
        self.pacman: Pacman = pacman

        self.algorithm: DepthFirstSearch = algorithm
        self._shortest_path_to_goal: list[tuple[int, int]] | None = None

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line_pos, self.column_pos = self.starting_position

    def change_goal(self, new_goal: tuple[int, int]) -> None:
        self.algorithm.exit = new_goal

    def change_entry_position(self) -> None:
        self.algorithm.entry = (self.line_pos, self.column_pos)

    def find_shortest_path_to_exit(self) -> None:
        self._shortest_path_to_goal = self.algorithm.solver()

    @property
    def shortest_path_to_goal(self) -> list[tuple[int, int]] | None:
        if self._shortest_path_to_goal is None:
            raise ValueError(
                f"{type(self).__name__} doesn't have a path to its goal")

        return self._shortest_path_to_goal

    def run_away(self) -> tuple[int, int]:
        if self.pacman.line_pos <= len(maze.cases) // 2:
            if self.pacman.column_pos <= len(maze.cases[0]) // 2:
                return (0, 0)
            else:
                return (0, maze.nb_column - 1)
        else:
            if self.pacman.column_pos <= len(maze.cases[0]) // 2:
                return (maze.nb_line - 1, 0)
            else:
                return (maze.nb_line - 1, maze.nb_column - 1)

    def chase_pacman(self) -> tuple[int, int]:
        return (self.pacman.line_pos, self.pacman.column_pos)


class Shadow(Ghost):  # red chase

    def __init__(self, maze: Maze, starting_position: tuple[int, int],
                 pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, starting_position, pacman,
                         super_pacgum_cooldown, algorithm)

    def get_goal(self) -> tuple[int, int]:
        if self.state == Character.State.RUNNING:
            return self.run_away()

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        return (0, 0)


class Speedy(Ghost):  # pink flank

    def __init__(self, maze: Maze, starting_position: tuple[int, int],
                 pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, starting_position, pacman,
                         super_pacgum_cooldown, algorithm)

    def get_goal(self) -> tuple[int, int]:
        if self.state == Character.State.RUNNING:
            return self.run_away()

        for cardinal_point in Direction:
            if self.pacman.last_move_direction == cardinal_point:
                for i in range(3, 0, -1):
                    new_line_pos = cardinal_point.value[0] * i
                    new_column_pos = cardinal_point.value[1] * i

                    if self.maze.is_accessible(new_line_pos, new_column_pos):
                        return (new_line_pos, new_column_pos)

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        return (0, maze.nb_column)


class Bashful(Ghost):  # cyan random

    def __init__(self, maze: Maze, starting_position: tuple[int, int],
                 pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, starting_position, pacman,
                         super_pacgum_cooldown, algorithm)

    def get_goal(self) -> tuple[int, int]:
        if self.state == Character.State.RUNNING:
            return self.run_away()

        new_line = -1
        new_column = -1

        while not self.maze.is_accessible(new_line, new_column):
            new_line = random.randint(0, self.maze.nb_line)
            new_column = random.randint(0, self.maze.nb_column)
        return (new_line, new_column)

    def _set_starting_position(self) -> tuple[int, int]:
        return (maze.nb_line, 0)


class Pokey(Ghost):  # orange chase + run away

    def __init__(self, maze: Maze, starting_position: tuple[int, int],
                 pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, starting_position, pacman,
                         super_pacgum_cooldown, algorithm)

    def is_pacman_too_close(self) -> bool:
        if (self.line_pos - self.pacman.line_pos < 3 and
           self.line_pos - self.pacman.line_pos > -3):
            if (self.column_pos - self.pacman.column_pos < 3 and
               self.column_pos - self.pacman.column_pos > -3):
                return True
        return False

    def get_goal(self) -> tuple[int, int]:
        if self.state == Character.State.RUNNING or self.is_pacman_too_close():
            return self.run_away()
        else:
            return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        return (maze.nb_line, maze.nb_column)


if __name__ == "__main__":
    maze = Maze()
    algo = DepthFirstSearch((3, 3), (0, 0), maze)
    pacman = Pacman(3, maze, 10)
    ghost = Ghost(maze, (1, 1), pacman, 10, algo)
