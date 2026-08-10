from .maze import Maze


class Player():
    def __init__(self, maze: Maze, lives: int = 3) -> None:
        self.lives: int = lives

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
