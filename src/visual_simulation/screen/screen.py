from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Screen(ABC):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        self.simulation_manager: "SimulationManager" = simulation_manager

    @abstractmethod
    def display_screen(self) -> None: ...

    def main_menu_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.main_menu.display_screen

    def victory_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.victory.display_screen

    def game_over_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_over.display_screen

    def game_play_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen

    def leaderboard_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.leaderboard.display_screen

    def pause_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.pause_menu.display_screen

    def instructions_screen(self) -> None:
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.instructions.display_screen

    def exit_game(self) -> None:
        self.simulation_manager.active = False

    def make_button(self,
                    pos: tuple[int, int],
                    text: pygame.Surface,
                    action: Callable[[], None],
                    px: int,
                    py: int) -> None:
        width = text.get_width() + px
        height = text.get_height() + py
        position = (pos[0] - width // 2, pos[1])
        self.draw_rectangle(position, width, height, (120, 78, 91))
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

    def draw_text(self, text: pygame.Surface,
                  width_adjust: int = 0,
                  height_adjust: int = 0) -> None:
        """Draw text into the simulation"""
        x, y = self.get_text_pos(
            text, width_adjust=width_adjust, height_adjust=height_adjust)

        self.simulation_manager.screen.blit(text, (x, y))

    def get_text_pos(self, text: pygame.Surface,
                     width_adjust: int = 0,
                     height_adjust: int = 0) -> tuple[int, int]:
        return (
            self.simulation_manager.screen_width // 2 -
            (text.get_width() // 2) + width_adjust,
            self.simulation_manager.screen_height // 2 -
            (text.get_height() // 2) + height_adjust)

    def draw_rectangle(self, coord: tuple[int, int],
                       width: int, height: int,
                       color: tuple[int, int, int],
                       center_width: bool = False,
                       center_height: bool = False) -> None:
        modified_coord = [coord[0], coord[1]]
        if center_width is True:
            modified_coord[0] -= width // 2
        if center_height is True:
            modified_coord[1] -= height // 2
        for actual_width in range(width):
            for actual_height in range(height):
                self.simulation_manager.screen.set_at(
                    ((actual_width + modified_coord[0]),
                     (actual_height + modified_coord[1])), color)
