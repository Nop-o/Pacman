from ..maze import Maze, Direction
from enum import Enum


class Entity:

    class State(Enum):
        HUNTING = 0
        RUNNING = 1

    def __init__(self, line: int, column: int, maze: Maze,
                 super_pacgum_cooldown: int) -> None:
        self.line: int = line
        self.column: int = column
        self.maze: Maze = maze
        self.super_pacgum_cooldown: int = super_pacgum_cooldown
        self.state: Entity.State = self.State.RUNNING

    def go_left(self) -> None:
        """Go one case left in the maze"""
        if self.maze.is_travelable(maze.cases[self.line][self.column],
                                   Direction.W):
            self.line = self.line - 1

    def go_right(self) -> None:
        """Go one case right in the maze"""
        if self.maze.is_travelable(maze.cases[self.line][self.column],
                                   Direction.E):
            self.line = self.line + 1

    def go_up(self) -> None:
        """Go one case up in the maze"""
        if self.maze.is_travelable(maze.cases[self.line][self.column],
                                   Direction.N):
            self.column = self.column - 1

    def go_down(self) -> None:
        """Go one case down in the maze"""
        if self.maze.is_travelable(maze.cases[self.line][self.column],
                                   Direction.S):
            self.column = self.column + 1

    def change_state(self) -> None:
        """Alternate the state between hunting and running for entities"""
        if self.state == self.State.HUNTING:
            self.state = self.State.RUNNING
        else:
            self.state = self.State.HUNTING

    def reset_super_pacgum_cooldown(self) -> None:
        """Reset the timer of the super pacgum effect"""
        self.super_pacgum_cooldown = self.super_pacgum_cooldown


if __name__ == "__main__":
    maze = Maze()
    entity = Entity(10, 10, maze, 10)
    print(entity.state)
