from .screen import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GameOver(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.user_name = ""

    def display_screen(self) -> None:
        self.simulation_manager.screen.fill((0, 0, 0))
        self.handle_user_writing()

        congrat_message = \
            self.simulation_manager.text_rendering.render_small_title(
                "You lost", (255, 255, 255))

        input_prompt = \
            self.simulation_manager.text_rendering.render_regular_text(
                "Enter your name to save your score", (255, 255, 255))

        user_name = \
            self.simulation_manager.text_rendering.render_regular_text(
                self.user_name, (255, 255, 255))

        button_text = \
            self.simulation_manager.text_rendering.render_regular_text(
                "Save Highscore", (255, 255, 255))

        congrat_pos = self.get_text_pos(congrat_message, height_adjust=-100)
        prompt_pos = self.get_text_pos(input_prompt, height_adjust=50)
        user_name_pos = self.get_text_pos(user_name, height_adjust=100)
        button_pos = self.get_text_pos(button_text, height_adjust=175)

        self.simulation_manager.screen.blit(congrat_message, congrat_pos)
        self.simulation_manager.screen.blit(input_prompt, prompt_pos)
        self.simulation_manager.screen.blit(user_name, user_name_pos)

        self.make_button(button_pos, button_text, self.leaderboard_screen,
                         50, 20)

    def button_action(self) -> None:
        self.simulation_manager.screen_manager.leaderboard.add_new_highscore(
            self.simulation_manager.game_state.score, self.user_name)
        self.leaderboard_screen()

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
