from .entity import Entity
from ..maze.maze import Maze


class Pacman(Entity):

    def __init__(self, line: int, column: int, lives: int, maze: Maze,
                 starting_position: tuple[int, int],
                 super_pacgum_cooldown: int) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown)
        self.starting_position: tuple[int, int] = self._set_starting_position()
        self.lives: int = lives
        self._last_move_direction: str = self.reset_last_move_direction()

    def _set_starting_position(self) -> tuple[int, int]:
        """Find the starting position of pacman, at the middle if possible"""
        line = (len(self.maze.cases) - 1) // 2
        column = (len(self.maze.cases[0]) - 1) // 2
        if self.verif_position(line, column):
            return (line, column)
        i = 1
        while True:
            j = 0
            while j < i:
                if self.verif_position(line-i + j, column-i):
                    return (line-i + j, column-i)
                if self.verif_position(line-i, column-i + j):
                    return (line-i, column-i + j)
                if self.verif_position(line+i + j, column-i):
                    return (line+i + j, column-i)
                if self.verif_position(line+i, column-i + j):
                    return (line+i, column-i + j)
                j += 1
            i += 1

    def verif_position(self, line: int, column: int) -> bool:
        if self.maze.cases[line][column].is_enclosed is False:
            self.line = line
            self.column = column
            return True
        return False

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line, self.column = self.starting_position

    @property
    def last_move_direction(self) -> str:
        return self._last_move_direction

    def reset_last_move_direction(self) -> None:
        self._last_move_direction = 'N'


if __name__ == "__main__":
    maze = Maze([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    pacman = Pacman(1, 1, 3, maze, (2, 2), 10)
    print(pacman.starting_position)
