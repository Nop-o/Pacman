from abc import ABC, abstractmethod
from .. import SimulationManager
from .screen import (GameOver, GamePlay, HUD, LeaderBoard,
                     MainMenu, PauseMenu, Victory)

class Screen(ABC):
    def __init__(self, simulation_manager: SimulationManager) -> None:
        self.simulation_manager: SimulationManager = simulation_manager

    @abstractmethod
    def display_screen(self) -> bool: ...

    @abstractmethod
    def event_manager(self) -> bool: ...

    def exit_game(self) -> bool:
        return False

    def go_to_main_menu(self) -> None:
        self.simulation_manager = self.main_menu.display_screen

    def resume_game(self) -> None:
        self.simulation_manager = self.game_play.display_screen

    def show_leaderboard(self) -> None:
        self.simulation_manager = self.leaderboard.display_screen

    def start_game(self) -> None:
        self.simulation_manager = self.game_play.display_screen
