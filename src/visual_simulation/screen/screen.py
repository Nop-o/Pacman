from abc import ABC, abstractmethod
import pygame

from typing import TYPE_CHECKING, Callable, Any

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Screen(ABC):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font | None,
                 big_font: pygame.font.Font | None) -> None:
        if font is None:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = font
        if big_font is None:
            self.big_font = pygame.font.Font(None, 80)
        else:
            self.big_font = big_font
        self.simulation_manager: "SimulationManager" = simulation_manager

    @abstractmethod
    def display_screen(self) -> None: ...

    def go_to_main_menu(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.main_menu.display_screen

    def resume_game(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen

    def go_to_victory_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.victory.display_screen

    def start_game(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen

    def exit_game(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_over.display_screen

    def go_to_leaderboard(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.leaderboard.display_screen

    def make_button(self,
                    pos: tuple[int, int],
                    text: pygame.Surface,
                    action: Callable,
                    px: int,
                    py: int) -> None:
        width = text.get_width() + px
        height = text.get_height() + py
        position = (pos[0] - width // 2, pos[1])
        self.simulation_manager.draw_rectangle(
            position, width, height, (120, 78, 91))
        text_pos = (
            position[0] + (width // 2) - (text.get_width() // 2),
            position[1] + (height // 2) - (text.get_height() // 2)
        )
        self.simulation_manager.screen.blit(text, text_pos)

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
                action()

    def draw_text(self, text: str, x: int, y: int,
                  color: pygame.Color = pygame.Color("gray44"),
                  font: pygame.font.Font | None = None,
                  center: bool = True) -> None:
        """Draw text into the simulation"""
        if font is None:
            font = self.font

        surface = font.render(text, True, color)
        if center:
            x -= surface.get_width() // 2
            y -= surface.get_height() // 2
        self.simulation_manager.screen.blit(surface, (x, y))
