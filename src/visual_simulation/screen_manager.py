from .screen import (GameOver, GamePlay, HUD, LeaderBoard, MainMenu,
                     PauseMenu, Victory, Instructions, LaunchGame)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .simulation_manager import SimulationManager


class ScreenManager:
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        self.leaderboard: LeaderBoard = LeaderBoard(
            simulation_manager=simulation_manager)
        self.game_over: GameOver = GameOver(
            simulation_manager=simulation_manager)
        self.hud: HUD = HUD(
            simulation_manager=simulation_manager)
        self.game_play: GamePlay = GamePlay(
            hud=self.hud,
            simulation_manager=simulation_manager)
        self.main_menu: MainMenu = MainMenu(
            simulation_manager=simulation_manager)
        self.pause_menu: PauseMenu = PauseMenu(
            simulation_manager=simulation_manager)
        self.victory: Victory = Victory(simulation_manager=simulation_manager)
        self.instructions: Instructions = Instructions(
            simulation_manager=simulation_manager)
        self.launch_game: LaunchGame = LaunchGame(
            simulation_manager=simulation_manager)
