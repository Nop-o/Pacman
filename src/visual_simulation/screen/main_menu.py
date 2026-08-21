from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class MainMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.current_choice_position: int = 0

    def show_instructions(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        self.simulation_manager.screen.fill((0, 0, 0))

        choices = ["game_play_screen", "leaderboard_screen",
                   "show_instructions", "exit_game"]

        test_message = self.simulation_manager.text_rendering.render_small_title(
            "main_menu", (255, 255, 255)
            )

        current_choice = \
            self.simulation_manager.text_rendering.render_small_title(
                f"current choice: {choices[self.current_choice_position]}",
                (255, 255, 255))

        test_message_pos = self.get_text_pos(test_message, height_adjust=-200)
        current_choice_pos = self.get_text_pos(current_choice)

        self.simulation_manager.screen.blit(test_message, test_message_pos)
        self.simulation_manager.screen.blit(current_choice, current_choice_pos)


    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        actions: list[Callable[[], None]] = [
            self.game_play_screen,
            self.leaderboard_screen,
            self.show_instructions,
            self.exit_game,
        ]

        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.current_choice_position < 3:
                        self.current_choice_position += 1
                    else:
                        self.current_choice_position = 0

                if event.key == pygame.K_UP:
                    if self.current_choice_position > 0:
                        self.current_choice_position -= 1
                    else:
                        self.current_choice_position = 3

                if event.key == pygame.K_RETURN:
                    actions[self.current_choice_position]()
                    return
