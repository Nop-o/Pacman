from .screen import Screen
from .leaderboard import LeaderBoard
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GameOver(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 leaderboard: LeaderBoard,
                 font: pygame.font.Font = pygame.font.Font(None, 80),
                 name_font: pygame.font.Font = pygame.font.Font(None, 30)
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, name_font=name_font)
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
