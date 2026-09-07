from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LaunchGame(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

        self.logo: pygame.Surface = self.sprite.get_sprite(
            "src/png/logo_sprite.png", 54, 554, 35, 35
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

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
