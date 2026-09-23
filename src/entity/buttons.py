from src.entity.sprite import Sprite
import pygame
import sys
import os


class Button(Sprite):
    """A single clickable/visual button backed by a sprite."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the button's sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        self.sprite: pygame.Surface = self.get_sprite(
            file_path, x, y, width, height)


class ButtonManager(Sprite):
    """Manage and render the joystick and menu buttons on screen."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Initialize joystick and menu button sprites and positions.

        Args:
            screen_width: Width of the screen in pixels.
            screen_height: Height of the screen in pixels.
        """
        path_joystick = self.resource_path("png/joystick.png")
        path_base = self.resource_path("png/joystick_base.png")
        self.joystick_sprites: list[Button] = [
            Button(path_joystick, 340, 145, 110, 90),
            Button(path_joystick, 240, 245, 110, 90),
            Button(path_joystick, 140, 145, 110, 90),
            Button(path_joystick, 240, 30, 110, 110),
        ]
        self.joystick_base_sprite: Button = Button(
            path_base, 102, 36, 172, 88)
        path = self.resource_path("png/entities_sprite.png")
        self.buttons_sprite: list[Button] = [
            Button(path, 201, 704, 35, 35),
            Button(path, 201, 796, 35, 35),
            ]

        self.screen_width: int = screen_width
        self.height: int = screen_height

        self.joystick_positions: list[tuple[int, int]] = \
            self._get_joystick_position()

    def _get_joystick_position(self) -> list[tuple[int, int]]:
        """Compute the on-screen position for each joystick direction sprite.

        Returns:
            A list of (x, y) positions, one per joystick direction.
        """
        original_x: int = self.screen_width - (self.screen_width // 6)
        original_y: int = self.height - (self.height // 4)

        return [
            (original_x + 27, original_y + 25),
            (original_x + 3, original_y + 29),
            (original_x - 20, original_y + 25),
            (original_x + 2, original_y),
        ]

    def get_button_positions(
       self, texts: list[pygame.Surface], paddings: list[int]
       ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Compute left and right arrow button positions for each menu text.

        Args:
            texts: Rendered text surfaces for each menu entry.
            paddings: Vertical padding to apply for each menu entry.

        Returns:
            A list of (left_arrow_position, right_arrow_position) pairs,
            one per menu entry after the first.
        """
        text_height: int = (texts[1].get_height() // 2) - 10

        return [(
            self.get_left_arrow_pos(texts[i], paddings[i] + text_height),
            self.get_right_arrow_pos(texts[i], paddings[i] + text_height))
            for i in range(1, len(texts))]

    def get_left_arrow_pos(
       self, text: pygame.Surface, height: int) -> tuple[int, int]:
        """Compute the position of the left arrow button next to a text.

        Args:
            text: Rendered text surface the arrow is positioned relative to.
            height: Vertical position for the arrow.

        Returns:
            The (x, y) position of the left arrow.
        """
        return (
            (self.screen_width // 2) - ((text.get_width() // 2) + 55), height)

    def get_right_arrow_pos(
       self, text: pygame.Surface, height: int) -> tuple[int, int]:
        """Compute the position of the right arrow button next to a text.

        Args:
            text: Rendered text surface the arrow is positioned relative to.
            height: Vertical position for the arrow.

        Returns:
            The (x, y) position of the right arrow.
        """
        return (
            (self.screen_width // 2) + ((text.get_width() // 2) + 20), height)

    def display_joystick(self, screen: pygame.Surface, direction: int) -> None:
        """Draw the joystick base and directional sprite on screen.

        Args:
            screen: Surface to draw on.
            direction: Index of the joystick direction sprite to display.
        """
        x: int = self.screen_width - (self.screen_width // 6) - 34
        y: int = self.height - (self.height // 4) + 50

        screen.blit(self.joystick_base_sprite.sprite, (x, y))
        screen.blit(self.joystick_sprites[direction].sprite,
                    self.joystick_positions[direction])

    def display_buttons(
       self, screen: pygame.Surface, texts: list[pygame.Surface],
       paddings: list[int], position: int) -> None:
        """Draw the left and right arrow buttons for the selected menu entry.

        Args:
            screen: Surface to draw on.
            texts: Rendered text surfaces for each menu entry.
            paddings: Vertical padding to apply for each menu entry.
            position: Index of the currently selected menu entry.
        """
        button_positions: list[tuple[tuple[int, int], tuple[int, int]]] = \
            self.get_button_positions(texts, paddings)

        screen.blit(
            self.buttons_sprite[0].sprite, button_positions[position][0])
        screen.blit(
            self.buttons_sprite[1].sprite, button_positions[position][1])

    @staticmethod
    def resource_path(relative_path: str) -> str:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)
