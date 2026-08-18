from . import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Victory(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.font: pygame.font.Font = pygame.font.Font(None, 80)
        self.name_font: pygame.font.Font = pygame.font.Font(None, 30)
        self.user_name = ""

    def display_screen(self) -> None:
        if not self.simulation_manager.key_pressed is None:
            if self.simulation_manager.key_pressed.isprintable():
                self.user_name += self.simulation_manager.key_pressed
        congrat_message = self.font.render(
            "Congratulation", 1, (255, 255, 255)
            )
        user_name = self.name_font.render(
            self.user_name, 1, (255, 255, 255)
        )
        input_prompt = self.name_font.render(
            "Enter your name to save your score",
            1,
            (255, 255, 255)
        )
        self.simulation_manager.screen.fill((0, 0, 0))
        congrat_pos = (
            self.simulation_manager.width - (congrat_message.get_width() // 2),
            self.simulation_manager.height // 2 - 100)
        self.simulation_manager.screen.blit(congrat_message, congrat_pos)
        prompt_pos = (
            self.simulation_manager.width - (input_prompt.get_width() // 2),
            congrat_pos[1] + 150
        )
        self.simulation_manager.screen.blit\
            (input_prompt, prompt_pos)
        user_name_pos = (
            self.simulation_manager.width - (user_name.get_width() // 2),
            prompt_pos[1] + input_prompt.get_height() + 50
        )
        self.simulation_manager.screen.blit(user_name, user_name_pos)
        button_pos = (
            self.simulation_manager.width // 2,
            user_name_pos[1] + user_name.get_height() + 75
        )
        self._make_button(button_pos)

    def _make_button(self, position):
        button_text = self.name_font.render(
            "Save Highscore",
            1,
            (255, 255, 255)
        )
        width = button_text.get_width() + 50
        height = button_text.get_height() + 20
        position[0] = position[0] - width // 2
        self.simulation_manager.draw_rectangle(
            position, width, height, (120, 78, 91))
        text_pos = (
            position[0] + (width // 2) - \
                (button_text.get_width() // 2),
            position[1] + (height // 2) - \
                (button_text.get_height() // 2)
        )
        self.simulation_manager.screen.blit(button_text, text_pos)

        if self.simulation_manager.mouse_click is not None:
            mouse_height = False
            mouse_width = False
            mouse_pos = self.simulation_manager.mouse_click
            if mouse_pos[0] >= position[0] and \
                mouse_pos[0] <= position[0] + width:
                mouse_width = True
            if mouse_pos[1] >= position[1] and \
                mouse_pos[1] <= position[1] + height:
                mouse_height = True
            if mouse_width is True and mouse_height is True:
                self.simulation_manager.state_to_call = \
                    self.screen_manager.leaderboard.display_screen\
                        (self.user_name)
