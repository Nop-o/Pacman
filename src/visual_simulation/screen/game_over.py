from .screen import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GameOver(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)
        self.user_name = ""

    def _handle_keyboard_input(self) -> None:
        if self.simulation_manager.key_pressed is not None:
            if self.simulation_manager.key_pressed.isprintable():
                self.user_name += self.simulation_manager.key_pressed
            if self.simulation_manager.delete_pressed is True:
                self.user_name = self.user_name[0:-1]

    def display_screen(self) -> None:
        self._handle_keyboard_input()

        congrat_message = self.big_font.render(
            "You lost", 1, (255, 255, 255)
            )
        input_prompt = self.font.render(
            "Enter your name to save your score",
            1,
            (255, 255, 255)
        )
        user_name = self.font.render(
            self.user_name, 1, (255, 255, 255)
        )
        button_text = self.font.render(
            "Save Highscore",
            1,
            (255, 255, 255)
        )

        self.simulation_manager.screen.fill((0, 0, 0))

        congrat_pos = self.get_text_pos(congrat_message, height_adjust=-100)
        prompt_pos = self.get_text_pos(input_prompt, height_adjust=50)
        user_name_pos = self.get_text_pos(user_name, height_adjust=100)
        button_pos = self.get_text_pos(button_text, height_adjust=175)

        self.simulation_manager.screen.blit(congrat_message, congrat_pos)
        self.simulation_manager.screen.blit(input_prompt, prompt_pos)
        self.simulation_manager.screen.blit(user_name, user_name_pos)

        self.make_button(button_pos, button_text,
                         self.leaderboard_screen,
                         50,
                         20)

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
