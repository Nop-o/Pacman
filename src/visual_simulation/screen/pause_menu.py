from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class PauseMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)
        self.current_choice_position: int = 0

    def display_screen(self) -> None:  # TODO
        pass

    def screen_selector(self) -> None:
        actions: list[Callable] = [
            self.game_play_screen,
            self.main_menu_screen,
            self.exit_game,
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.current_choice_position < 2:
                        self.current_choice_position += 1
                    else:
                        self.current_choice_position = 0

                if event.key == pygame.K_UP:
                    if self.current_choice_position > 0:
                        self.current_choice_position -= 1
                    else:
                        self.current_choice_position = 2

                if event.key == pygame.K_RETURN:
                    actions[self.current_choice_position]()
                    return
