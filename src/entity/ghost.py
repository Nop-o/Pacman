from .entity import Entity
from ..maze.maze import Maze


class Ghost(Entity):

    def __init__(self, line: int, column: int, maze: Maze,
                 starting_position: tuple[int, int],
                 super_pacgum_cooldown: int) -> None:
        super().__init__(
            line, column, maze, super_pacgum_cooldown)
        self.starting_position: tuple[int, int] = starting_position

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line, self.column = self.starting_position


if __name__ == "__main__":
    maze = Maze([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    ghost = Ghost(1, 1, maze, (1, 1), 10)
    print(ghost.starting_position)
