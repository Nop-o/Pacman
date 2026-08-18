from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class MainMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

    def show_instructions(self) -> None:  # TODO
        pass

    def display_screen(self) -> bool:  # TODO
        pass

    def event_manager(self) -> bool:
        actions: list[Callable] = [
            self.resume_game,
            self.show_leaderboard,
            self.show_instructions,
            self.exit_game,
        ]
        position: int = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if position < 3:
                        position = position + 1
                    else:
                        position = 0

                if event.key == pygame.K_UP:
                    if position > 0:
                        position = position - 1
                    else:
                        position = 3

                if event.key == pygame.K_RETURN:
                    return actions[position]()

        return False
