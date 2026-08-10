class Case():
    def __init__(self, case: int) -> None:
        self.wall_north: bool = False
        self.wall_east: bool = False
        self.wall_south: bool = False
        self.wall_west: bool = False
        self.create_walls(case)
        self.is_enclosed: bool = True
        if any([self.wall_west, self.wall_south,
                self.wall_east, self.wall_north]):
            self.is_enclosed = False

    def create_walls(self, case: int) -> None:
        binary = bin(case)[2:]
        while len(binary) < 4:
            binary = "0" + binary
        if int(binary[0]) == 1:
            self.wall_west = True
        if int(binary[1]) == 1:
            self.wall_south = True
        if int(binary[2]) == 1:
            self.wall_east = True
        if int(binary[3]) == 1:
            self.wall_north = True
