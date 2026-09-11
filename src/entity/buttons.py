from src.entity.sprite import Sprite
import pygame


class Button(Sprite):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        self.sprite: pygame.Surface = self.get_sprite(
            file_path, x, y, width, height)


class ButtonManager(Sprite):
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.joystick_sprites: list[Button] = [
            Button("png/joystick.png", 340, 145, 110, 90),
            Button("png/joystick.png", 240, 245, 110, 90),
            Button("png/joystick.png", 140, 145, 110, 90),
            Button("png/joystick.png", 240, 30, 110, 110),
        ]

        self.buttons_sprite: list[Button] = [
            self.get_sprite("png/entities_sprite.png", 201, 704, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 754, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 796, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 654, 35, 35),
            ]

        self.width: int = screen_width
        self.height: int = screen_height

        self.joystick_positions: list[tuple[int, int]] = self._get_joystick_position()

    def _get_joystick_position(self) -> list[tuple[int, int]]:
        original_x: int = self.width - (self.width // 6)
        original_y: int = self.height - (self.height // 4)

        return [
            (original_x + 27, original_y + 25),
            (original_x + 3, original_y + 29),
            (original_x - 20, original_y + 25),
            (original_x + 2, original_y),
        ]

    def display_joystick(self, screen: pygame.Surface, direction: int) -> None:
        screen.blit(self.joystick_sprites[direction].sprite,
                    self.joystick_positions[direction])

