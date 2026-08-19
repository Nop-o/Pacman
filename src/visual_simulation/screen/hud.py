from . import Screen
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class HUD(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)

    def show_score(self) -> None:  # TODO
        pass

    def show_lives(self) -> None:  # TODO
        pass

    def show_level(self) -> None:  # TODO
        pass

    def show_timer(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        pass
