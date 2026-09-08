import pygame
import time
from time import sleep
from enum import Enum

class Entities:

    class Direction(Enum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Entities")

        self.screen_height: int
        self.screen_width: int
        self.screen: pygame.Surface = self._adjust_screen_size()

        self.active: bool = True
        self.frame_time: float = 0.15
        self.movement_time: float = 0.15
        self.frame_count: int = 0
        self.extra_pixel: int = 4

        self.current_direction: Entities.Direction = Entities.Direction.RIGHT

        self.shadow_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", self.extra_pixel,
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", self.extra_pixel, 100 +
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", self.extra_pixel, 200 +
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", self.extra_pixel, 300 +
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.shadow_position: tuple[int, int] = (
            self.extra_pixel, self.extra_pixel)
        
        self.speedy_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 50 + self.extra_pixel,
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 50 + self.extra_pixel,
             100 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 50 + self.extra_pixel,
             200 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 50 + self.extra_pixel,
             300 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.speedy_position: tuple[int, int] = (
            50 + self.extra_pixel, self.extra_pixel)

        self.bashful_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 100 + self.extra_pixel,
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 100 + self.extra_pixel,
             100 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 100 + self.extra_pixel,
             200 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 100 + self.extra_pixel,
             300 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.bashful_position: tuple[int, int] = (
            100 + self.extra_pixel, self.extra_pixel)

        self.pokey_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 150 + self.extra_pixel,
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 150 + self.extra_pixel,
             100 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 150 + self.extra_pixel,
             200 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 150 + self.extra_pixel,
             300 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.pokey_position: tuple[int, int] = (
            150 + self.extra_pixel, self.extra_pixel)

        self.pacman_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 850 + self.extra_pixel,
             self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 850 + self.extra_pixel,
             150 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 850 + self.extra_pixel,
             300 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 850 + self.extra_pixel,
             450 + self.extra_pixel + (i * 50), 35, 35)
             for i in range(0, 3, 1)]]
        self.pacman_position: tuple[int, int] = (
            200 + self.extra_pixel, self.extra_pixel)

    def launch_simulation(self) -> None:
        frame_time_elapse: float = 0.0
        movement_time_elapse: float = 0.0

        while self.active:
            start_time = time.monotonic()

            if not self.active:
                pygame.quit()
                break

            self.event_manager()
            self.display_entities()

            if frame_time_elapse > self.frame_time:
                frame_time_elapse -= self.frame_time
                self.frame_count += 1

            if movement_time_elapse > self.movement_time:
                movement_time_elapse -= self.movement_time
                self.update_entities_pos()

            if self.frame_count == 60:
                self.frame_count = 0

            frame_time_elapse += time.monotonic() - start_time
            movement_time_elapse += time.monotonic() - start_time


    def display_entities(self) -> None:
        self.screen.fill(pygame.Color("black"))

        self.screen.blit(self.shadow_sprites[self.current_direction.value][
            self.frame_count % 2], self.shadow_position)
        self.screen.blit(self.speedy_sprites[self.current_direction.value][
            self.frame_count % 2], self.speedy_position)
        self.screen.blit(self.bashful_sprites[self.current_direction.value][
            self.frame_count % 2], self.bashful_position)
        self.screen.blit(self.pokey_sprites[self.current_direction.value][
            self.frame_count % 2], self.pokey_position)
        self.screen.blit(self.pacman_sprites[self.current_direction.value][
            self.frame_count % 3], self.pacman_position)

        pygame.display.flip()
    
    def update_entities_pos(self) -> None:
        self.shadow_position = self.speedy_position
        self.speedy_position = self.bashful_position
        self.bashful_position = self.pokey_position
        self.pokey_position = self.pacman_position
        self.pacman_position = tuple(a + b for a, b in zip(self.pacman_position, self.get_direction_value()))

        pacman_x, pacman_y = self.pacman_position
        if self.screen_width <= pacman_x + 35:
            self.pacman_position = tuple(a - b for a, b in zip(
                self.pacman_position, (self.screen_width, 0)))
        elif self.extra_pixel >= pacman_x - 35:
            self.pacman_position = tuple(a + b for a, b in zip(
                self.pacman_position, (self.screen_width, 0)))
        elif self.screen_height <= pacman_y + 35:
            self.pacman_position = tuple(a - b for a, b in zip(
                self.pacman_position, (0, self.screen_height)))
        elif self.extra_pixel > pacman_y + 35:
            self.pacman_position = tuple(a + b for a, b in zip(
                self.pacman_position, (0, self.screen_height)))

    def get_direction_value(self) -> tuple[int, int]:
        if self.current_direction == self.Direction.UP:
            return (0, -50)
        elif self.current_direction == self.Direction.DOWN:
            return (0, 50)
        elif self.current_direction == self.Direction.LEFT:
            return (-50, 0)
        return (50, 0)

    @staticmethod
    def mlx_get_screen_size() -> tuple[int, int]:
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def _adjust_screen_size(self) -> pygame.Surface:
        """Resize the pygame window so it fits within the physical display."""
        screen_width, screen_height = self.mlx_get_screen_size()

        self.screen_height = screen_height
        self.screen_width = screen_width

        return pygame.display.set_mode((screen_width, screen_height))

    def event_manager(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.active = False
                break

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and
                   self.current_direction not in [Entities.Direction.RIGHT,
                                               Entities.Direction.LEFT]):
                    self.previous_direction = self.current_direction
                    self.current_direction = self.Direction.LEFT
                if (event.key == pygame.K_RIGHT and
                   self.current_direction not in [Entities.Direction.RIGHT,
                                               Entities.Direction.LEFT]):
                    self.previous_direction = self.current_direction
                    self.current_direction = self.Direction.RIGHT
                if (event.key == pygame.K_DOWN and
                   self.current_direction not in [Entities.Direction.UP,
                                               Entities.Direction.DOWN]):
                    self.previous_direction = self.current_direction
                    self.current_direction = self.Direction.DOWN
                if (event.key == pygame.K_UP and
                   self.current_direction not in [Entities.Direction.UP,
                                               Entities.Direction.DOWN]):
                    self.previous_direction = self.current_direction
                    self.current_direction = self.Direction.UP
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    break

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image


if __name__ == "__main__":
    simu = Entities()
    simu.launch_simulation()