from . import Entity
import pygame


class Cherry(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 4, 35, 35)


class Strawberry(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 54, 35, 35)


class Apricot(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 104, 35, 35)


class Apple(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 154, 35, 35)


class Berry(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 204, 35, 35)


class Banana(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 254, 35, 35)


class Peach(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 601, 304, 35, 35)
