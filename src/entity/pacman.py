from .entity import Entity
from ..maze import Maze


class Pacman(Entity):

    def __init__(self, line: int, column: int, lives: int, maze: Maze) -> None:
        super().__init__(line, column)
        self.lives = lives

    def set_starting_position(self, maze: Maze) -> None:
        line = (len(maze.cases) - 1) // 2
        column = (len(maze.cases[0]) - 1) // 2
        if self.verif_position(maze, line, column):
            return
        i = 1
        while True:
            j = 0
            while j < i:
                if self.verif_position(maze, line-i + j, column-i):
                    return
                if self.verif_position(maze, line-i, column-i + j):
                    return
                if self.verif_position(maze, line+i + j, column-i):
                    return
                if self.verif_position(maze, line+i, column-i + j):
                    return
                j += 1
            i += 1

    def verif_position(self, maze: Maze, line: int, column: int)\
            -> bool:
        if maze.cases[line][column].is_enclosed is False:
            self.line = line
            self.column = column
            return True
        return False
