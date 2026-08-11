from .case import Case
from mazegenerator import MazeGenerator


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
                self.cases[i].append(Case(column))

    def is_travelable(self, case: Case, direction: str) -> bool:
        if direction == "N":
            if case.wall_north is True:
                return True
        elif direction == "E":
            if case.wall_east is True:
                return True
        elif direction == "S":
            if case.wall_south is True:
                return True
        elif direction == "W":
            if case.wall_west is True:
                return True
        else:
            raise ValueError("Error in is_tavelable: "
                             "The direction is invalide")
        return False
