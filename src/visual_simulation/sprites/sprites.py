import pygame


class Sprites:

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(file_path, (0, 0), (x, y, width, height))

        return image
