from . import Screen
import pygame
from typing import TYPE_CHECKING
from ...entity import Character, FruitManager
import time

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LaunchGame(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

        self.current_direction_choice: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

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
        self.shadow_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

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
        self.speedy_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

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
        self.bashful_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

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
        self.pokey_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

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
        self.pacman_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

        self.ghost_running_away_sprites: list[pygame.Surface] = [
            self.get_sprite("png/entities_sprite.png", 1, 554 + (i * 50),
                            35, 35)
            for i in range(0, 2, 1)]
        self.ghost_running_away_sprites.extend(
            [self.get_sprite("png/entities_sprite.png", 51, 554 + (i * 50),
                             35, 35)
             for i in range(0, 2, 1)])

        self._init_entity_starting_pos()

        self.old_pacman_logo: pygame.Surface = self.get_sprite(
            "png/old_pacman_logo.png", 30, 100, 1250, 500)
        self.old_pacman_logo_pos: tuple[int, int] = (
            self.simulation_manager.get_center_width(self.old_pacman_logo),
            self.simulation_manager.screen_height // 8)

        self.welcome_text: pygame.Surface = \
            self.simulation_manager.text_rendering.render_small_title(
                "Press RETURN to enter the game ...", (255, 255, 0))
        self.welcome_text_pos: tuple[int, int] = (
            0, self.simulation_manager.screen_height // 3)

        self.ghost_chasing: bool = True

        self.max_super_pacgum_cooldown: float = 1.5
        self.current_super_pacgum_cooldown: float = 0.0
        self.blinking_ghost_time: float = 1.0

        self.fruit_manager: FruitManager = FruitManager()
        self._set_fruit_positions()

        self.movement_time: float = 0.06
        self.movement_time_elapse: float = 0.0

    def _init_entity_starting_pos(self) -> None:
        x_middle = self.simulation_manager.screen_width // 2
        y_middle = self.simulation_manager.screen_height // 2

        pacman_x: int = x_middle - x_middle // 6
        pacman_y: int = y_middle + y_middle // 6

        self.pacman_position = self.snap_to_grid((pacman_x, pacman_y))

        self.shadow_position = self.snap_to_grid((pacman_x - 50, pacman_y))
        self.speedy_position = self.snap_to_grid((pacman_x - 100, pacman_y))
        self.pokey_position = self.snap_to_grid((pacman_x - 150, pacman_y))
        self.bashful_position = self.snap_to_grid((pacman_x - 200, pacman_y))

    def display_images(self) -> None:
        self.display_entities()

        self.simulation_manager.screen.blit(
            self.old_pacman_logo, self.old_pacman_logo_pos)
        self.draw_text(self.welcome_text, self.welcome_text_pos[0],
                       self.welcome_text_pos[1])

    def display_screen(self) -> None:
        start_time: float = time.monotonic()

        self.simulation_manager.dipslay_sky()
        self.display_images()

        if self.movement_time_elapse > self.movement_time:
            self.movement_time_elapse -= self.movement_time
            self.update_entities_pos()

        if (self.ghost_chasing and self.pacman_position ==
           self.fruit_manager.fruit_position):
            self.fruit_manager.ate_fruit()
            self.update_ghost_chasing()
            self.reverse_current_direction_choice()

        if not self.ghost_chasing:
            self.update_super_pacgum_cooldown(start_time)

        self.movement_time_elapse += time.monotonic() - start_time

    def update_ghost_chasing(self) -> None:
        if self.ghost_chasing:
            self.ghost_chasing = False
        else:
            self.ghost_chasing = True

    def reverse_current_direction_choice(self) -> None:
        if self.current_direction_choice == Character.FacingDirection.UP:
            self.current_direction_choice = Character.FacingDirection.DOWN
        elif self.current_direction_choice == Character.FacingDirection.DOWN:
            self.current_direction_choice = Character.FacingDirection.UP
        elif self.current_direction_choice == Character.FacingDirection.RIGHT:
            self.current_direction_choice = Character.FacingDirection.LEFT
        else:
            self.current_direction_choice = Character.FacingDirection.RIGHT

    def _set_fruit_positions(self) -> None:
        x_middle = self.simulation_manager.screen_width // 2
        y_middle = self.simulation_manager.screen_height // 2

        self.fruit_manager.set_fruit_position([
            self.snap_to_grid(
                (x_middle - x_middle // 3, y_middle + y_middle // 4)),
            self.snap_to_grid(
                (x_middle + x_middle // 3, y_middle + y_middle // 4)),
        ])

    def update_super_pacgum_cooldown(self, start_time: float) -> None:
        self.current_super_pacgum_cooldown += time.monotonic() - start_time

        if self.current_super_pacgum_cooldown > self.max_super_pacgum_cooldown:
            self.current_super_pacgum_cooldown = 0
            self.update_ghost_chasing()
            self.reverse_current_direction_choice()

    def display_entities(self) -> None:
        if self.ghost_chasing:
            self.display_default_entities()
        else:
            self.display_pacman_hunting_entities()

    def display_default_entities(self) -> None:
        ghost_list: list[str] = ["shadow", "speedy", "bashful", "pokey"]

        for ghost in ghost_list:
            sprites = getattr(self, ghost + "_sprites")
            direction = getattr(self, ghost + "_direction")
            position = getattr(self, ghost + "_position")

            self.simulation_manager.screen.blit(sprites[direction][
                self.simulation_manager.frame_count % 2], position)

        self.simulation_manager.screen.blit(self.pacman_moving_sprites[
            self.pacman_direction][
                self.simulation_manager.frame_count % 3], self.pacman_position)

        self.fruit_manager.display_fruits(self.simulation_manager.screen)

    def display_pacman_hunting_entities(self) -> None:
        if self.current_super_pacgum_cooldown < self.blinking_ghost_time:
            image_count = 2
        else:
            image_count = 4

        self.simulation_manager.screen.blit(self.ghost_running_away_sprites[
            self.simulation_manager.frame_count % image_count],
            self.shadow_position)
        self.simulation_manager.screen.blit(self.ghost_running_away_sprites[
            self.simulation_manager.frame_count % image_count],
            self.speedy_position)
        self.simulation_manager.screen.blit(self.ghost_running_away_sprites[
            self.simulation_manager.frame_count % image_count],
            self.bashful_position)
        self.simulation_manager.screen.blit(self.ghost_running_away_sprites[
            self.simulation_manager.frame_count % image_count],
            self.pokey_position)
        self.simulation_manager.screen.blit(self.pacman_moving_sprites[
            self.pacman_direction][self.simulation_manager.frame_count % 3],
            self.pacman_position)

    def travel_back_to_opposite_screen_side(self) -> None:
        for attr in ("pacman_position", "shadow_position", "speedy_position",
                     "bashful_position", "pokey_position"):
            pos_x, pos_y = getattr(self, attr)

            if self.simulation_manager.screen_width <= pos_x + 35:
                setattr(self, attr, tuple(a - b for a, b in zip(
                    (pos_x, pos_y), (self.simulation_manager.screen_width, 0)))
                    )
            elif 4 >= pos_x - 35:
                setattr(self, attr, tuple(a + b for a, b in zip(
                    (pos_x, pos_y), (self.simulation_manager.screen_width, 0))
                    ))
            elif self.simulation_manager.screen_height <= pos_y + 35:
                setattr(self, attr, tuple(a - b for a, b in zip(
                    (pos_x, pos_y), (0, self.simulation_manager.screen_height))
                    ))
            elif 4 > pos_y + 35:
                setattr(self, attr, tuple(a + b for a, b in zip(
                    (pos_x, pos_y), (0, self.simulation_manager.screen_height))
                    ))
            setattr(self, attr, self.snap_to_grid(getattr(self, attr)))

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image

    def update_entities_pos(self) -> None:
        if self.ghost_chasing:
            entity_order = ["shadow", "speedy", "bashful", "pokey", "pacman"]
        else:
            entity_order = ["pacman", "pokey", "bashful", "speedy", "shadow"]

        for i in range(0, len(entity_order) - 1, 1):
            setattr(self, entity_order[i] + "_direction", getattr(
                self, entity_order[i + 1] + "_direction"))
            setattr(self, entity_order[i] + "_position", getattr(
                self, entity_order[i + 1] + "_position"))

        setattr(self, entity_order[-1] + "_direction", getattr(
            self, "current_direction_choice"))
        setattr(self, entity_order[-1] + "_position",
                tuple(a + b for a, b in zip(getattr(
                    self, entity_order[-1] + "_position"),
                    self.get_direction_value(self.current_direction_choice))))

        self.travel_back_to_opposite_screen_side()

    def get_direction_value(
       self, direction: Character.FacingDirection) -> tuple[int, int]:
        if direction == Character.FacingDirection.UP:
            return (0, -50)
        elif direction == Character.FacingDirection.DOWN:
            return (0, 50)
        elif direction == Character.FacingDirection.LEFT:
            return (-50, 0)
        return (50, 0)

    def snap_to_grid(self, position: tuple[int, int],
                     case_size: int = 50) -> tuple[int, int]:
        x, y = position
        return (round(x / case_size) * case_size,
                round(y / case_size) * case_size)

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
                if (event.key == pygame.K_LEFT and
                        self.current_direction_choice not in [
                            Character.FacingDirection.RIGHT,
                            Character.FacingDirection.LEFT]):
                    self.current_direction_choice = \
                        Character.FacingDirection.LEFT
                if (event.key == pygame.K_RIGHT and
                        self.current_direction_choice not in [
                            Character.FacingDirection.RIGHT,
                            Character.FacingDirection.LEFT]):
                    self.current_direction_choice = \
                        Character.FacingDirection.RIGHT
                if (event.key == pygame.K_DOWN and
                        self.current_direction_choice not in [
                            Character.FacingDirection.UP,
                            Character.FacingDirection.DOWN]):
                    self.current_direction_choice = \
                        Character.FacingDirection.DOWN
                if (event.key == pygame.K_UP and
                        self.current_direction_choice not in [
                            Character.FacingDirection.UP,
                            Character.FacingDirection.DOWN]):
                    self.current_direction_choice = \
                        Character.FacingDirection.UP
