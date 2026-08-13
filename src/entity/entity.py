from abc import ABC

class Entity(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.line_pos: int
        self.column_pos: int

    def get_coord(self) -> tuple[int, int]:
        return (self.line_pos, self.column_pos)