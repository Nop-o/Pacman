from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class MainMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.current_choice_position: int = 0

    def display_screen(self) -> None:
        self.simulation_manager.dipslay_sky()

        screen_titles: list[pygame.Surface] = [
            self.simulation_manager.text_rendering.render_big_title(
                "Main Menu", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_medium_title(
                "Start Game", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_medium_title(
                "View Highscores", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_medium_title(
                "Instructions", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_medium_title(
                "Exit Game", (255, 255, 0))
        ]

        title_padding: list[int] = self.get_title_paddings(
            screen_titles, 10, 6
        )

        self.simulation_manager.display_menu_sprites()

        self.display_titles(self.simulation_manager.screen,
                            screen_titles, title_padding)

        self.simulation_manager.button_manager.display_buttons(
            self.simulation_manager.screen, screen_titles,
            title_padding, self.current_choice_position
        )

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        actions: list[Callable[[], None]] = [
            self.new_game,
            self.leaderboard_screen,
            self.instructions_screen,
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
