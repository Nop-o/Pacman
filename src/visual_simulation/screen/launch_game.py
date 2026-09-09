from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LaunchGame(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

        self.logo: pygame.Surface = self.get_sprite(
            "png/old_pacman_logo.png", 54, 554, 35, 35
        )  # TODO : adjust the variable

    def display_screen(self) -> None:
        self.simulation_manager.screen.fill((0, 0, 0))

        pacman_title = \
            self.simulation_manager.text_rendering.render_big_pacman(
                "PAC-MAN", (255, 255, 0))
        welcome_text = \
            self.simulation_manager.text_rendering.render_small_title(
                "Press RETURN to enter the game ...", (255, 255, 255))

        self.draw_text(pacman_title, width_adjust=0, height_adjust=-165)
        self.draw_text(welcome_text, width_adjust=0, height_adjust=200)

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
