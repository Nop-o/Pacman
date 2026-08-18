from .screen import Screen
from .leaderboard import LeaderBoard
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GameOver(Screen):
    def __init__(self, leaderboard: LeaderBoard,
                 simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.leaderboard: LeaderBoard = LeaderBoard

    def display_screen(self) -> None:  # TODO
        pass

    def event_manager(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.got_to_leaderboard()
                    return

