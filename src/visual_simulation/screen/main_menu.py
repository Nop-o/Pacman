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
        self.simulation_manager.dipslay_sky()

        choices = ["game_play_screen", "leaderboard_screen",
                   "show_instructions", "exit_game"]

        main_menu_title = \
            self.simulation_manager.text_rendering.render_small_title(
                "Main Menu", (255, 255, 255))
        start_game_text = \
            self.simulation_manager.text_rendering.render_big_text(
                "Start Game", (255, 255, 255))
        leaderboard_text = \
            self.simulation_manager.text_rendering.render_big_text(
                "View Highscores", (255, 255, 255))
        instructions_text = \
            self.simulation_manager.text_rendering.render_big_text(
                "Instructions", (255, 255, 255))
        exit_game_text = \
            self.simulation_manager.text_rendering.render_big_text(
                "Exit Game", (255, 255, 255))
        current_choice_text = \
            self.simulation_manager.text_rendering.render_small_title(
                f"current choice: {choices[self.current_choice_position]}",
                (255, 255, 255))

        self.draw_text(main_menu_title, width_adjust=0, height_adjust=-300)
        self.draw_text(start_game_text, width_adjust=0, height_adjust=100)
        self.draw_text(leaderboard_text, width_adjust=0, height_adjust=-300)
        self.draw_text(instructions_text, width_adjust=0, height_adjust=100)
        self.draw_text(exit_game_text, width_adjust=0, height_adjust=100)
        self.draw_text(current_choice_text, width_adjust=0, height_adjust=100)

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
