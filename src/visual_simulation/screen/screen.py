from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager
    from ..screen_manager import ScreenManager


class Screen(ABC):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        self.simulation_manager: "SimulationManager" = simulation_manager

    @abstractmethod
    def display_screen(self) -> None: ...

    def go_to_main_menu(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.main_menu.display_screen

    def resume_game(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen

    def show_victory_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.victory.display_screen

    def start_game(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen
