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
            self.get_sprite("png/entities_sprite.png", 201, 796, 35, 35),
            ]

        self.screen_width: int = screen_width
        self.height: int = screen_height

        self.joystick_positions: list[tuple[int, int]] = \
            self._get_joystick_position()

    def _get_joystick_position(self) -> list[tuple[int, int]]:
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
        text_height: int = (texts[1].get_height() // 2 ) - 10

        return [(
            self.get_left_arrow_pos(texts[i], paddings[i] + text_height),
            self.get_right_arrow_pos(texts[i], paddings[i] + text_height))
            for i in range(1, len(texts))]

    def get_left_arrow_pos(
       self, text: pygame.Surface, height: int) -> tuple[int, int]:
        return ((self.screen_width // 2) - ((text.get_width() // 2) + 55), height)

    def get_right_arrow_pos(
       self, text: pygame.Surface, height: int) -> tuple[int, int]:
        return ((self.screen_width // 2) + ((text.get_width() // 2) + 20), height)

    def display_joystick(self, screen: pygame.Surface, direction: int) -> None:
        screen.blit(self.joystick_sprites[direction].sprite,
                    self.joystick_positions[direction])

    def display_buttons(
       self, screen: pygame.Surface, texts: list[pygame.Surface],
       paddings: list[int], position: int) -> None:
        button_positions: list[tuple[tuple[int, int], tuple[int, int]]] = \
            self.get_button_positions(texts, paddings)

        screen.blit(self.buttons_sprite[0], button_positions[position][0])
        screen.blit(self.buttons_sprite[1], button_positions[position][1])
