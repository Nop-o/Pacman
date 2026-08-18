from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class MainMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font = pygame.font.Font(None, 80),
                 name_font: pygame.font.Font = pygame.font.Font(None, 30)
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, name_font=name_font)

    def show_instructions(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        pass

    def event_manager(self) -> None:
        actions: list[Callable] = [
            self.resume_game,
            self.got_to_leaderboard,
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
                    actions[position]()
