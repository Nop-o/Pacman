from . import Entity


class Pacgum(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos = line_pos
        self.column_pos = column_pos
