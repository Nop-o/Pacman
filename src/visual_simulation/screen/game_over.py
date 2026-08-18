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

    def display_screen(self) -> bool:  # TODO
        pass

    def event_manager(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.show_leaderboard()

        return False
