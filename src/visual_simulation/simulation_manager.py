from time import time, sleep
import pygame
from typing import Any, Callable
from .screen_manager import ScreenManager
from ..game_state import GameState
from .screen import Level


class SimulationManager():
    def __init__(self, json_data: dict[str, Any]) -> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.fps: int = 60
        self.frame_duration: float = 1.0 / self.fps
        self.height: int = 1000
        self.width: int = 1500
        self.screen: pygame.Surface = pygame.display.set_mode((1500, 1000))
        # TODO set basic function to main menu
        self.active: bool = True

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.delete_pressed = False
        self.key_pressed: str | None = None
        self.mouse_click: tuple[int, int] | None = None

        self.current_level: Level = Level(self)
        self.game_state: GameState = GameState(**json_data)
        self.screen_manager: ScreenManager = ScreenManager(
            self, self.current_level)
        self.state_to_call: Callable = \
            self.screen_manager.main_menu.display_screen

    def launch(self) -> None:
        while self.active:
            start_time = time()

            self.event_manager()
            self.state_to_call()
            self.display_on_screen()
            self.reset_event()

            elapsed = time() - start_time
            if elapsed < self.frame_duration:
                sleep(self.frame_duration - elapsed)

    def clear_last_frame(self, color: str = "black") -> None:  # useless ?
        """Clear the last frame, recover it with a screen with a color"""
        self.screen.fill(pygame.Color(color))

    @staticmethod
    def display_on_screen() -> None:
        """Display everything that you prepared to the screen"""
        pygame.display.flip()

    def event_manager(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.active = False
            if event.type == pygame.KEYDOWN:
                self.key_pressed = event.unicode
                if event.key == pygame.K_ESCAPE:
                    self.active = (
                        self.screen_manager.pause_menu.display_screen())
                if (event.key == pygame.K_DELETE or
                        event.key == pygame.K_BACKSPACE):
                    self.delete_pressed = True
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                if event.key == pygame.K_DOWN:
                    self.down_pressed = True
                if event.key == pygame.K_UP:
                    self.up_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                if event.key == pygame.K_DOWN:
                    self.down_pressed = False
                if event.key == pygame.K_UP:
                    self.up_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click = event.pos

    def reset_event(self):
        self.key_pressed = None
        self.mouse_click = None
        self.delete_pressed = False

    def draw_rectangle(self, coord: tuple[int, int],
                       width: int, height: int,
                       color: tuple[int, int, int]) -> None:
        for actual_width in range(width):
            for actual_height in range(height):
                self.screen.set_at(
                    ((actual_width + coord[0]),
                     (actual_height + coord[1])), color)
