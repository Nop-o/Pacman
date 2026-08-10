from ..maze import Maze
from enum import Enum


class Entity:

    class State(Enum):
        HUNTING = 0
        RUNNING = 1

    def __init__(self, line: int, column: int, maze: Maze) -> None:
        self.line = line
        self.column = column
        self.maze = maze
        self.state = self.State.RUNNING

    def go_left(self) -> None:
        if self.maze.is_travelable(maze.cases[self.line][self.column], 'W'):
            self.line = self.line - 1

    def go_right(self) -> None:
        if self.maze.is_travelable(maze.cases[self.line][self.column], 'E'):
            self.line = self.line + 1

    def go_up(self) -> None:
        if self.maze.is_travelable(maze.cases[self.line][self.column], 'N'):
            self.column = self.column - 1

    def go_down(self) -> None:
        if self.maze.is_travelable(maze.cases[self.line][self.column], 'S'):
            self.column = self.column + 1

    def change_state(self) -> None:
        if self.state == self.State.HUNTING:
            self.state = self.State.RUNNING
        else:
            self.state = self.State.HUNTING


if __name__ == "__main__":
    maze = Maze([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    entity = Entity(10, 10, maze)
    print(entity.state)
