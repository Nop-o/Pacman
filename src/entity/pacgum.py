from . import Entity
import pygame


class Pacgum(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.pacgum_sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 404, 35, 35)

        self.super_pacgum_sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 454, 35, 35)
