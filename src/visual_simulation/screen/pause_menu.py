from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class PauseMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.current_choice_position: int = 0

    def display_screen(self) -> None:  # TODO
        choices = ["game_play_screen", "main_menu_screen", "exit_game"]

        test_message = self.font.render(
            "main_menu", 1, (255, 255, 255)
            )

        current_choice = self.big_font.render(
            f"current choice: {choices[self.current_choice_position]}", 1, (255, 255, 255)
            )

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        actions: list[Callable[[], None]] = [
            self.game_play_screen,
            self.main_menu_screen,
            self.exit_game,
        ]

        for event in events:
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
