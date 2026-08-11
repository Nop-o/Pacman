from .case import Case
from enum import Enum
from mazegenerator import MazeGenerator


class Direction(Enum):
    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)


class Maze():
    def __init__(self, seed: int = 0) -> None:
        self.cases: list[list[Case]] = []
        generator = MazeGenerator()
        generator.generate(seed)
        self.create_cases(generator.maze)

    def create_cases(self, cases: list[list[int]]) -> None:
        for i, line in enumerate(cases):
            self.cases.append([])
            for n, column in enumerate(line):
                self.cases[i].append(Case(column, i, n))

    def is_travelable(self, case: Case, direction: Direction) -> bool:
        if direction == Direction.N:
            if case.wall_north is True:
                return False
        elif direction == Direction.E:
            if case.wall_east is True:
                return False
        elif direction == Direction.S:
            if case.wall_south is True:
                return False
        elif direction == Direction.W:
            if case.wall_west is True:
                return True
        else:
            raise ValueError("Error in is_tavelable: "
                             "The direction is invalide")
        return False

    def is_accessible(self, line: int, column: int) -> bool:
        return not self.cases[line][column].is_enclosed
