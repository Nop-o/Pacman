from abc import ABC
import pygame


class Entity(ABC):
    def __init__(self) -> None:
        self.line_pos: int
        self.column_pos: int

    def get_coord(self) -> tuple[int, int]:
        return (self.line_pos, self.column_pos)

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image
