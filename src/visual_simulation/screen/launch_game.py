from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LaunchGame(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

    def display_screen(self) -> None:
        self.simulation_manager.screen.fill((0, 0, 0))

        pacman_title = \
            self.simulation_manager.text_rendering.render_big_pacman(
                "PAC-MAN", (255, 255, 0))
        welcome_text = \
            self.simulation_manager.text_rendering.render_small_title(
                "Press return to enter the game ...", (255, 255, 255))

        pacman_title_pos = self.get_text_pos(pacman_title, height_adjust=-165)
        welcome_text_pos = self.get_text_pos(welcome_text, height_adjust=200)

        self.simulation_manager.screen.blit(pacman_title, pacman_title_pos)
        self.simulation_manager.screen.blit(welcome_text, welcome_text_pos)

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
