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

    def display_screen(self) -> None:
        if self.simulation_manager.key_pressed is not None:
            if self.simulation_manager.key_pressed.isprintable():
                self.user_name += self.simulation_manager.key_pressed
            if self.simulation_manager.delete_pressed is True:
                self.user_name = self.user_name[0:-1]
        congrat_message = self.big_font.render(
            "You lost", 1, (255, 255, 255)
            )
        user_name = self.font.render(
            self.user_name, 1, (255, 255, 255)
        )
        input_prompt = self.font.render(
            "Enter your name to save your score",
            1,
            (255, 255, 255)
        )
        button_text = self.font.render(
            "Save Highscore",
            1,
            (255, 255, 255)
        )
        self.simulation_manager.screen.fill((0, 0, 0))
        congrat_pos = (
            self.simulation_manager.screen_width // 2 -
            (congrat_message.get_width() // 2),
            self.simulation_manager.screen_height // 2 - 100)
        self.simulation_manager.screen.blit(congrat_message, congrat_pos)
        prompt_pos = (
            self.simulation_manager.screen_width // 2 -
            (input_prompt.get_width() // 2),
            congrat_pos[1] + 150
        )
        self.simulation_manager.screen.blit(input_prompt, prompt_pos)
        user_name_pos = (
            self.simulation_manager.screen_width // 2 - (
                user_name.get_width() // 2),
            prompt_pos[1] + input_prompt.get_height() + 50
        )
        self.simulation_manager.screen.blit(user_name, user_name_pos)
        button_pos = (
            self.simulation_manager.screen_width // 2,
            user_name_pos[1] + user_name.get_height() + 75
        )
        self.make_button(button_pos, button_text,
                         self.leaderboard_screen,
                         50,
                         20)

    def button_action(self) -> None:
        self.simulation_manager.screen_manager.leaderboard.add_new_highscore(
            self.simulation_manager.game_state.score, self.user_name)
        self.leaderboard_screen()

    def screen_selector(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_screen
                    return
