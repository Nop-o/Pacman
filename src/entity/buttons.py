from . import Entity
import pygame


class Buttons(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.buttons_sprite: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 201, 704, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 754, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 796, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 654, 35, 35),
            ]
