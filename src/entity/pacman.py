from . import Character
from ..maze import Maze, Direction


class Pacman(Character):

    def __init__(self, lives: int, maze: Maze,
                 super_pacgum_cooldown: int) -> None:
        super().__init__(maze, super_pacgum_cooldown)
        self.starting_position: tuple[int, int] = self._set_starting_position()
        self.lives: int = lives
        self.reset_last_move_direction()

    def _set_starting_position(self) -> tuple[int, int]:
        """Find the starting position of pacman, at the middle if possible"""
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
        if self.maze.cases[line_pos][column_pos].is_enclosed is False:
            self.line_pos = line_pos
            self.column_pos = column_pos
            return True
        return False

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line_pos, self.column_pos = self.starting_position

    @property
    def last_move_direction(self) -> Direction:
        return self._last_move_direction

    def reset_last_move_direction(self) -> None:
        self._last_move_direction = Direction.N


if __name__ == "__main__":
    maze = Maze()
