from abc import ABC
import sys, os
import pygame


class Entity(ABC):
    """Abstract base class for objects positioned within the maze grid."""

    def __init__(self) -> None:
        """Declare the entity's grid position attributes."""
        self.line_pos: int
        self.column_pos: int

    def get_coord(self) -> tuple[int, int]:
        """Return the entity's current (line, column) position.

        Returns:
            The entity's grid coordinates.
        """
        return (self.line_pos, self.column_pos)

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

    @staticmethod
    def resource_path(relative_path: str) -> str:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)
