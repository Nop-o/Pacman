from . import Screen, Level
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

        self.shadow_position: tuple[int, int]
        self.speedy_position: tuple[int, int]
        self.bashful_position: tuple[int, int]
        self.pokey_position: tuple[int, int]
        self.pacman_position: tuple[int, int]

        self._init_entity_starting_pos()

        self.old_pacman_logo: pygame.Surface = self.get_sprite(
            "png/old_pacman_logo.png", 30, 100, 1250, 500)
        self.old_pacman_logo_pos: tuple[int, int] = (
            self.get_center_width(self.old_pacman_logo),
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
        level: Level = self.simulation_manager.screen_manager.game_play.level

        for ghost, ghost_name in zip(level.ghosts, ghost_list):
            sprites = getattr(ghost, "sprites")
            direction = getattr(ghost, "direction")
            position = getattr(self, ghost_name + "_position")

            self.simulation_manager.screen.blit(sprites[direction][
                self.simulation_manager.frame_count % 2], position)

        self.simulation_manager.screen.blit(level.pacman.sprites[
            level.pacman.direction][self.simulation_manager.frame_count % 3],
            self.pacman_position)

        self.fruit_manager.display_fruits(self.simulation_manager.screen)

    def display_pacman_hunting_entities(self) -> None:
        level: Level = self.simulation_manager.screen_manager.game_play.level

        if self.current_super_pacgum_cooldown < self.blinking_ghost_time:
            image_count = 2
        else:
            image_count = 4

        self.simulation_manager.screen.blit(
            level.ghosts[0].running_away_sprites[
                self.simulation_manager.frame_count % image_count],
            self.shadow_position)
        self.simulation_manager.screen.blit(
            level.ghosts[1].running_away_sprites[
                self.simulation_manager.frame_count % image_count],
            self.speedy_position)
        self.simulation_manager.screen.blit(
            level.ghosts[2].running_away_sprites[
                self.simulation_manager.frame_count % image_count],
            self.bashful_position)
        self.simulation_manager.screen.blit(
            level.ghosts[3].running_away_sprites[
                self.simulation_manager.frame_count % image_count],
            self.pokey_position)
        self.simulation_manager.screen.blit(
            level.pacman.sprites[level.pacman.direction][
                self.simulation_manager.frame_count % 3],
            self.pacman_position)

    def travel_back_to_opposite_screen_side(self) -> None:
        screen_width : int = self.simulation_manager.screen_width 
        screen_height : int = self.simulation_manager.screen_height 
        for attr in ("pacman_position", "shadow_position", "speedy_position",
                     "bashful_position", "pokey_position"):
            pos_x, pos_y = getattr(self, attr)

            if screen_width <= pos_x:
                pos_x -= screen_width 
            elif 0 >= pos_x:
                pos_x += screen_width

            if screen_height <= pos_y + 60:
                pos_y -= screen_height
            elif 0 >= pos_y:
                pos_y += screen_height

            setattr(self, attr, self.snap_to_grid((pos_x, pos_y)))

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image

    def update_entities_pos(self) -> None:
        level: Level = self.simulation_manager.screen_manager.game_play.level

        if self.ghost_chasing:
            entity_order = [level.ghosts[3], level.ghosts[2], level.ghosts[1],
                            level.ghosts[0], level.pacman]
            entity_name_order = ["shadow", "speedy", "bashful",
                                 "pokey", "pacman"]
        else:
            entity_order = [level.pacman, level.ghosts[3], level.ghosts[2],
                            level.ghosts[1], level.ghosts[0]]
            entity_name_order = ["pacman", "pokey", "bashful",
                                 "speedy", "shadow"]

        for i in range(0, len(entity_order) - 1, 1):
            entity_order[i].direction = entity_order[i + 1].direction
            setattr(self, entity_name_order[i] + "_position", getattr(
                self, entity_name_order[i + 1] + "_position"))

        entity_order[-1].direction = self.current_direction_choice
        setattr(self, entity_name_order[-1] + "_position",
                self.add_two_tuple(getattr(
                    self, entity_name_order[-1] + "_position"),
                    self.get_direction_value(self.current_direction_choice)))

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
