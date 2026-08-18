from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class PauseMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

    def display_screen(self) -> bool:  # TODO
        pass

    def event_manager(self) -> bool:
        actions: list[Callable] = [
            self.resume_game,
            self.go_to_main_menu,
            self.exit_game,
        ]
        position: int = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if position < 2:
                        position = position + 1
                    else:
                        position = 0

                if event.key == pygame.K_UP:
                    if position > 0:
                        position = position - 1
                    else:
                        position = 2

                if event.key == pygame.K_RETURN:
                    return actions[position]()

        return False
