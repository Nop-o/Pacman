from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Victory(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.user_name = ""

    def display_screen(self) -> None:
        self.simulation_manager.dipslay_sky()

        game_over_text = \
            self.simulation_manager.text_rendering.render_small_title(
                "VICTORY", (255, 255, 255))

        if self.is_score_in_leaderboard() is True:
            self.handle_user_writing()

            text_prompt = \
                self.simulation_manager.text_rendering.render_regular_text(
                    "Enter your name to save your score", (255, 255, 255))

            user_name = \
                self.simulation_manager.text_rendering.render_regular_text(
                    self.user_name, (255, 255, 255))
            button_text = \
                self.simulation_manager.text_rendering.render_regular_text(
                    "Save Highscore", (255, 255, 255))

            self.draw_text(user_name, width_adjust=0, height_adjust=100)

            button_pos = self.get_text_pos(button_text, height_adjust=175)
            self.make_button(
                button_pos, button_text, self.button_action, 50, 20)

        else:
            text_prompt = \
                self.simulation_manager.text_rendering.render_regular_text(
                    "Press RETURN to go back to main menu ...", (255, 255, 255)
                    )

        self.draw_text(game_over_text, width_adjust=0, height_adjust=-100)
        self.draw_text(text_prompt, width_adjust=0, height_adjust=50)

    def is_score_in_leaderboard(self) -> bool:
        return (
            self.simulation_manager.game_state.score >
            self.simulation_manager.screen_manager.leaderboard.scores[9])

    def button_action(self) -> None:
        self.simulation_manager.screen_manager.leaderboard.add_new_highscore(
            self.simulation_manager.game_state.score, self.user_name)
        self.leaderboard_screen()

    def handle_user_writing(self) -> None:
        if self.simulation_manager.key_pressed is not None:
            if self.simulation_manager.key_pressed.isprintable():
                self.user_name += self.simulation_manager.key_pressed
            if self.simulation_manager.delete_pressed is True:
                self.user_name = self.user_name[0:-1]

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return
