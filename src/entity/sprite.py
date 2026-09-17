import pygame


class Sprite:
    """Mixin providing sprite sheet region extraction."""

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        """Extract a sprite region from a sprite sheet image.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.

        Returns:
            A surface containing the extracted sprite, with alpha channel.
        """
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image
