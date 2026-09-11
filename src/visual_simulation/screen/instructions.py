from . import Screen
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Instructions(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

    def display_screen(self) -> None:  # TODO
        self.simulation_manager.dipslay_sky()

        test_message = \
            self.simulation_manager.text_rendering.render_small_title(
                "Instructions", (255, 255, 255))

        test_message_pos = self.get_text_pos(test_message, height_adjust=-200)
        self.simulation_manager.screen.blit(test_message, test_message_pos)

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
