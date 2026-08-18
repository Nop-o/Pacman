from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Victory(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.font: pygame.font.Font = pygame.font.Font(None, 80)

    def display_screen(self) -> None:  # TODO
        self.simulation_manager.screen.fill((0, 0, 0))
        congrat_message = self.font.render(
            "Congratulation", 1, (255, 255, 255)
            )
        self.simulation_manager.screen.blit(congrat_message,
                                            (750 - congrat_message.get_width(),
                                             400))
