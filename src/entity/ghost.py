from .entity import Entity
from ..maze.maze import Maze
from ..algorithm.dfs import DepthFirstSearch
from .pacman import Pacman
import random


class Ghost(Entity):

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int], pacman: Pacman,
                 super_pacgum_cooldown: int, algorithm: DepthFirstSearch
                 ) -> None:
        super().__init__(line, column, maze, super_pacgum_cooldown)

        self.starting_position: tuple[int, int] = starting_position
        self.pacman: Pacman = pacman

        self.algorithm: DepthFirstSearch = algorithm
        self._shortest_path_to_goal: list[tuple[int, int]] | None = None

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line, self.column = self.starting_position

    def change_goal(self, new_goal: tuple[int, int]) -> None:
        self.algorithm.exit = new_goal

    def change_entry_position(self, new_start: tuple[int, int]) -> None:
        self.algorithm.entry = (self.line, self.column)

    def find_shortest_path_to_exit(self) -> None:
        self._shortest_path_to_goal = self.algorithm.solver()

    @property
    def shortest_path_to_goal(self) -> list[tuple[int, int]] | None:
        if self._shortest_path_to_goal is None:
            raise ValueError(
                f"{type(self).__name__} doesn't have a path to its goal")

        return self._shortest_path_to_goal

    def run_away(self) -> None:  # TODO
        pass

    def chase_pacman(self) -> None:  # TODO
        pass


class Shadow(Ghost):  #red chase

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int], pacman: Pacman,
                 super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown, starting_position,
            pacman, algorithm)

    def get_goal(self) -> tuple[int, int]:
        new_line = -1
        new_column = -1
        while not self.maze.is_accessible(new_line, new_column):
            new_line = random.randint(0, self.maze.width)
            new_column = random.randint(0, self.maze.height)
        return (new_line, new_column)


class Speedy(Ghost):  #pink flank

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int], pacman: Pacman,
                 super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown, starting_position,
            pacman, algorithm)

    def get_goal(self) -> tuple[int, int]:
        pass


class Bashful(Ghost):  #cyan random

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int], pacman: Pacman,
                 super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown, starting_position,
            pacman, algorithm)

    def get_goal(self) -> tuple[int, int]:
        new_line = -1
        new_column = -1

        while not self.maze.is_accessible(new_line, new_column):
            new_line = random.randint(0, self.maze.width)
            new_column = random.randint(0, self.maze.height)
        return (new_line, new_column)


class Pokey(Ghost):  #orange chase + run away

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int], pacman: Pacman,
                 super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown, starting_position,
            pacman, algorithm)

    def is_pacman_too_close(self) -> bool:
        if (self.line - self.pacman.line < 3 and
           self.line - self.pacman.line > -3):
            if (self.column - self.pacman.column < 3 and
               self.column - self.pacman.column > -3):
                return True
        return False

    def get_goal(self) -> tuple[int, int]:
        if self.is_pacman_too_close():
            self.run_away()
        else:
            self.chase_pacman()


if __name__ == "__main__":
    algo = DepthFirstSearch(3, 3, 0, 0)
    maze = Maze([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    ghost = Ghost(1, 1, maze, (1, 1), 10)
    print(ghost.starting_position)
