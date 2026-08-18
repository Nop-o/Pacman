from .screen import Screen
from .hud import HUD
from .level import Level
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GamePlay(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 level: Level, hud: HUD,
                 font: pygame.font.Font = pygame.font.Font(None, 80),
                 name_font: pygame.font.Font = pygame.font.Font(None, 30)
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, name_font=name_font)
        self.level: Level = level
        self.hud: HUD = hud

    def display_screen(self) -> None:
        self.level.display_screen()
        self.hud.display_screen()

    def event_manager(self) -> None:  # TODO
        pass
