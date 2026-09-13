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
        generator: MazeGenerator = MazeGenerator()
        generator.generate(seed)
        self.create_cases(generator.maze)
        self.nb_line: int = len(self.cases)
        self.nb_column: int = len(self.cases[0])

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
                return False
        else:
            raise ValueError("Error in is_tavelable: "
                             "The direction is invalide")
        return True

    def get_adjacent_case(self, case: Case, direction: Direction)\
            -> Case | None:
        if self.is_travelable(case, direction):
            new_line = case.line_pos + direction.value[0]
            new_column = case.column_pos + direction.value[1]
            return self.cases[new_line][new_column]
        return None

    def get_neighbors(self, case: Case) -> list[Case]:
        neighbors: list[Case] = []
        for direction in Direction:
            adjacent_case = self.get_adjacent_case(case, direction)
            if adjacent_case is not None:
                neighbors.append(adjacent_case)
        return neighbors

    def is_accessible(self, line_pos: int, column_pos: int) -> bool:
        if line_pos < 0 or column_pos < 0:
            return False
        if line_pos > self.nb_line - 1 or column_pos > self.nb_column - 1:
            return False
        return not self.cases[line_pos][column_pos].is_enclosed

    def get_case(self, coord: tuple[int, int]) -> Case:
        return self.cases[coord[0]][coord[1]]

    def get_direction_between_case(self, case1: Case, case2: Case)\
            -> Direction | None:
        for direction in Direction:
            adjacent_case = self.get_adjacent_case(case1, direction)
            if adjacent_case == case2:
                return direction
        return None
