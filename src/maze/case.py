from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity import Pacgum


class Case():
    """A single cell of the maze, with walls and an optional pacgum."""

    def __init__(self, case: int, line_pos: int, column_pos: int) -> None:
        """Initialize a maze cell's walls and position.

        Args:
            case: Binary-encoded value describing which walls are present.
            line_pos: Line position of the cell in the maze.
            column_pos: Column position of the cell in the maze.
        """
        self.wall_north: bool = False
        self.wall_east: bool = False
        self.wall_south: bool = False
        self.wall_west: bool = False
        self.create_walls(case)
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos
        self.is_enclosed: bool = all([self.wall_west, self.wall_south,
                                      self.wall_east, self.wall_north])
        self.pacgum: Pacgum | None = None

    def create_walls(self, case: int) -> None:
        """Set the cell's walls based on its binary-encoded value.

        Args:
            case: Binary-encoded value describing which walls are present.
        """
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
        """Return the cell's position in the maze.

        Returns:
            The (line, column) position of the cell.
        """
        return (self.line_pos, self.column_pos)
