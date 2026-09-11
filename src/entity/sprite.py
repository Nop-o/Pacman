import pygame


class Sprite:
    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image
