from . import Screen
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Instructions(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)

    def display_screen(self) -> None:  # TODO
        test_message = self.big_font.render(
            "Instructions", 1, (255, 255, 255)
            )

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
