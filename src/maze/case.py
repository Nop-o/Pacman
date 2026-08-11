class Case():
    def __init__(self, case: int, line_pos: int, column_pos: int) -> None:
        self.wall_north: bool = False
        self.wall_east: bool = False
        self.wall_south: bool = False
        self.wall_west: bool = False
        self.create_walls(case)
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos
        self.is_enclosed: bool = all([self.wall_west, self.wall_south,
                                      self.wall_east, self.wall_north])

    def create_walls(self, case: int) -> None:
        """Create the walls of one case based on it's binary value"""
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

    def get_coordinate(self) -> tuple[int, int]:
        return (self.line_pos, self.column_pos)
