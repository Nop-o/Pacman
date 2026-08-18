from .screen import Screen
from .hud import HUD
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GamePlay(Screen):
    def __init__(
       self, level, hud: HUD, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.level = level
        self.hud: HUD = hud

    def display_screen(self) -> None:
        self.level.display_screen()
        self.hud.display_screen()

    def event_manager(self) -> None:  # TODO
        pass
