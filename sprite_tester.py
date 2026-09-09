import pygame
import time
from time import sleep
from enum import IntEnum
from typing import Any


class Entities:

    class Direction(IntEnum):
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

        self.ghost_chasing: bool = False
        self.current_choice: Entities.Direction = Entities.Direction.RIGHT

        self.shadow_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 1, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 1, 104 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 1, 204 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 1, 304 + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.shadow_position: tuple[int, int]
        self.shadow_direction: Entities.Direction = Entities.Direction.RIGHT
        
        self.speedy_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 51, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 51, 104 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 51, 204 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 51, 304 + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.speedy_position: tuple[int, int]
        self.speedy_direction: Entities.Direction = Entities.Direction.RIGHT

        self.bashful_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 101, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 101, 104 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 101, 204 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 101, 304 + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.bashful_position: tuple[int, int]
        self.bashful_direction: Entities.Direction = Entities.Direction.RIGHT

        self.pokey_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 151, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 151, 104 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 151, 204 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 151, 304 + (i * 50), 35, 35)
             for i in range(0, 2, 1)]]
        self.pokey_position: tuple[int, int]
        self.pokey_direction: Entities.Direction = Entities.Direction.RIGHT

        self.pacman_moving_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 851, 4 + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 851, 154 + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 851, 304 + (i * 50), 35, 35)
             for i in range(0, 3, 1)],
            [self.get_sprite(
             "png/entities_sprite.png", 851, 454 + (i * 50), 35, 35)
             for i in range(0, 3, 1)]]
        self.pacman_position: tuple[int, int]
        self.pacman_direction: Entities.Direction = Entities.Direction.RIGHT

        self._init_entity_starting_pos()

        self.pacman_dying_sprites: list[pygame.Surface] = \
            [self.get_sprite(
              "png/entities_sprite.png", 351, 4 + (i * 50), 35, 35)
              for i in range(0, 11, 1)]

        self.pacgum_sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 404, 35, 35)

        self.super_pacgum_sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 454, 35, 35)

        self.ghost_running_away_sprites: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 1, 554 + (i * 50), 35, 35)
            for i in range(0, 2, 1)]
        self.ghost_running_away_sprites.extend(
            [self.get_sprite("png/entities_sprite.png", 51, 554 + (i * 50), 35, 35)
             for i in range(0, 2, 1)])

        self.fruits_sprites: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 601, 4 + (i * 50), 35, 35)
            for i in range(0, 7, 1)]

        self.buttons_sprite: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 201, 704, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 754, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 796, 35, 35),
            self.get_sprite("png/entities_sprite.png", 201, 654, 35, 35),
            ]

        self.small_pacman_logo_sprite: pygame.Surface = self.get_sprite(
            "png/small_pacman_logo.png", 10, 120, 295, 75)

        self.small_pacman_logo_2_sprite: pygame.Surface = self.get_sprite(
            "png/small_pacman_logo_2.png", 14, 40, 800, 200)

        self.big_pacman_logo_sprite: pygame.Surface = self.get_sprite(
            "png/big_pacman_logo.png", 2, 2, 1550, 720)

        self.pacman_holding_ghost_sprite: pygame.Surface = self.get_sprite(
            "png/pacman_holding_ghost.png", 0, 0, 280, 192)

        self.arcade_pacman: pygame.Surface = self.get_sprite(
            "png/arcade_pacman.png", 50, 10, 380, 800)

        self.running_pacman: pygame.Surface = self.get_sprite(
            "png/running_pacman.png", 10, 0, 715, 800)

        self.old_pacman_logo: pygame.Surface = self.get_sprite(
            "png/old_pacman_logo.png", 30, 100, 10000, 10000)

        self.old_pacman_logo_big: pygame.Surface = self.get_sprite(
            "png/old_pacman_logo_big.png", 30, 100, 10000, 10000)

    def launch_simulation(self) -> None:
        frame_time_elapse: float = 0.0
        movement_time_elapse: float = 0.0

        while self.active:
            start_time = time.monotonic()

            if not self.active:
                pygame.quit()
                break

            self.screen.fill(pygame.Color("blue"))
            self.event_manager()
            self.display_entities()
            self.display_titles()
            pygame.display.flip()


            if frame_time_elapse > self.frame_time:
                frame_time_elapse -= self.frame_time
                self.frame_count += 1

            if movement_time_elapse > self.movement_time:
                movement_time_elapse -= self.movement_time
                self.update_entities_pos()

            if self.frame_count == 60:
                self.frame_count = 0

            current_time = time.monotonic()
            frame_time_elapse += current_time - start_time
            movement_time_elapse += current_time - start_time

    def display_default_entities(self) -> None:
        self.screen.blit(self.shadow_sprites[self.shadow_direction][
            self.frame_count % 2], self.shadow_position)
        self.screen.blit(self.speedy_sprites[self.speedy_direction][
            self.frame_count % 2], self.speedy_position)
        self.screen.blit(self.bashful_sprites[self.bashful_direction][
            self.frame_count % 2], self.bashful_position)
        self.screen.blit(self.pokey_sprites[self.pokey_direction][
            self.frame_count % 2], self.pokey_position)
        self.screen.blit(self.pacman_moving_sprites[self.pacman_direction][
            self.frame_count % 3], self.pacman_position)

    def _init_entity_starting_pos(self) -> None:
        if self.ghost_chasing:
            self.shadow_position = (950, 700)
            self.speedy_position = (1000, 700)
            self.pokey_position = (1100, 700)
            self.bashful_position = (1050, 700)
            self.pacman_position = (1150, 700)
        else:
            self.shadow_position = (1150, 700)
            self.speedy_position = (1100, 700)
            self.pokey_position = (1050, 700)
            self.bashful_position = (1000, 700)
            self.pacman_position = (950, 700)

    def display_pacman_hunting_entities(self) -> None:
        if self.frame_count < 30:
            image_count = 2
        else:
            image_count = 4


        self.screen.blit(self.ghost_running_away_sprites[
            self.frame_count % image_count], self.shadow_position)
        self.screen.blit(self.ghost_running_away_sprites[
            self.frame_count % image_count], self.speedy_position)
        self.screen.blit(self.ghost_running_away_sprites[
            self.frame_count % image_count], self.bashful_position)
        self.screen.blit(self.ghost_running_away_sprites[
            self.frame_count % image_count], self.pokey_position)
        self.screen.blit(self.pacman_moving_sprites[self.pacman_direction][
            self.frame_count % 3], self.pacman_position)

    def display_entities(self) -> None:
        if self.ghost_chasing:
            self.display_default_entities()
        else:
            self.display_pacman_hunting_entities()

        # self.screen.blit(self.super_pacgum_sprite, (50, 50))
        # self.screen.blit(self.pacgum_sprite, (50, 100))
        # self.screen.blit(self.ghost_running_away_sprites[self.frame_count % 4], (50, 250))
        # self.screen.blit(self.pacman_dying_sprites[self.frame_count % 11], (50, 200))

        # self.screen.blit(self.buttons_sprite[Entities.Direction.RIGHT], (150, 150))
        # self.screen.blit(self.buttons_sprite[Entities.Direction.DOWN], (100, 200))
        # self.screen.blit(self.buttons_sprite[Entities.Direction.LEFT], (50, 150))
        # self.screen.blit(self.buttons_sprite[Entities.Direction.UP], (100, 100))

        # self.screen.blit(self.fruits_sprites[self.frame_count % 7], (150, 200))

        # self.screen.blit(self.pacman_holding_ghost_sprite, (50, 300))
        # self.screen.blit(self.arcade_pacman, (50, 500))
        # self.screen.blit(self.running_pacman, (450, 400))

        # self.screen.blit(self.small_pacman_logo_sprite, (0, 0))
        # self.screen.blit(self.small_pacman_logo_2_sprite, (0, 100))
        # self.screen.blit(self.big_pacman_logo_sprite, (0, 300))
        # self.screen.blit(self.old_pacman_logo, (0, 700))

    def display_titles(self) -> None:

        # self.screen.blit(self.small_pacman_logo_sprite, (0, 0))
        # self.screen.blit(self.small_pacman_logo_2_sprite, (0, 100))
        # self.screen.blit(self.big_pacman_logo_sprite, (0, 300))
        # self.screen.blit(self.old_pacman_logo, (0, 700))

        # self.screen.blit(self.old_pacman_logo_big, (310, 50))
        # self.screen.blit(self.old_pacman_logo_big, (310, 50))
        self.screen.blit(self.old_pacman_logo, (500, 200))

    def update_entities_pos(self) -> None:
        if self.ghost_chasing:
            entity_order = ["shadow", "speedy", "bashful", "pokey", "pacman"]
        else:
            entity_order = ["pacman", "pokey", "bashful", "speedy", "shadow"]

        for i in range(0, len(entity_order) - 1, 1):
            setattr(self, entity_order[i] + "_direction", getattr(self, entity_order[i + 1] + "_direction"))
            setattr(self, entity_order[i] + "_position", getattr(self, entity_order[i + 1] + "_position"))

        setattr(self, entity_order[-1] + "_direction", getattr(self, "current_choice"))
        setattr(self, entity_order[-1] + "_position", tuple(a + b for a, b in zip(getattr(self, entity_order[-1] + "_position"), self.get_direction_value(self.current_choice))))

        self.travel_back_to_opposite_screen_side()

    def update_direction(self, old_pos: tuple[int, int],
                         new_pos: tuple[int, int]) -> Any:
        old_x, old_y = old_pos
        next_x, next_y = new_pos

        if old_x > next_x:
            direction = Entities.Direction.LEFT
        elif old_x < next_x:
            direction = Entities.Direction.RIGHT
        elif old_y > next_y:
            direction = Entities.Direction.UP
        else:
            direction = Entities.Direction.DOWN

        new_position = tuple(a + b for a, b in zip(
            old_pos, self.get_direction_value(direction)))

        return (direction, new_position)

    def travel_back_to_opposite_screen_side(self) -> None:
        for attr in ("pacman_position", "shadow_position", "speedy_position",
                     "bashful_position", "pokey_position"):
            pos_x, pos_y = getattr(self, attr)

            if self.screen_width <= pos_x + 35:
                setattr(self, attr, tuple(a - b for a, b in zip((pos_x, pos_y), (self.screen_width, 0))))
            elif 4 >= pos_x - 35:
                setattr(self, attr, tuple(a + b for a, b in zip((pos_x, pos_y), (self.screen_width, 0))))
            elif self.screen_height <= pos_y + 35:
                setattr(self, attr, tuple(a - b for a, b in zip((pos_x, pos_y), (0, self.screen_height))))
            elif 4 > pos_y + 35:
                setattr(self, attr, tuple(a + b for a, b in zip((pos_x, pos_y), (0, self.screen_height))))

    def get_direction_value(self, direction) -> tuple[int, int]:
        if direction == self.Direction.UP:
            return (0, -50)
        elif direction == self.Direction.DOWN:
            return (0, 50)
        elif direction == self.Direction.LEFT:
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

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image

    def event_manager(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.active = False
                break

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and
                   self.current_choice not in [Entities.Direction.RIGHT,
                                               Entities.Direction.LEFT]):
                    self.current_choice = self.Direction.LEFT
                if (event.key == pygame.K_RIGHT and
                   self.current_choice not in [Entities.Direction.RIGHT,
                                               Entities.Direction.LEFT]):
                    self.current_choice = self.Direction.RIGHT
                if (event.key == pygame.K_DOWN and
                   self.current_choice not in [Entities.Direction.UP,
                                               Entities.Direction.DOWN]):
                    self.current_choice = self.Direction.DOWN
                if (event.key == pygame.K_UP and
                   self.current_choice not in [Entities.Direction.UP,
                                               Entities.Direction.DOWN]):
                    self.current_choice = self.Direction.UP
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    break


if __name__ == "__main__":
    simu = Entities()
    simu.launch_simulation()