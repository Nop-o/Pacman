import time
import pygame
from typing import Any, Callable
from .screen_manager import ScreenManager
from .text_rendering import TextRendering
from ..game_state import GameState
from .screen import Level


class SimulationManager():
    def __init__(self, json_data: dict[str, Any]) -> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")

        self.frame_count: int = 0
        self.frame_time: float = 0.1

        self.fps: int = 60
        self.frame_duration: float = 1.0 / self.fps
        self.screen_height: int
        self.screen_width: int
        self.screen: pygame.Surface = self._adjust_screen_size()
        self.active: bool = True

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.delete_pressed = False
        self.key_pressed: str | None = None
        self.mouse_click: tuple[int, int] | None = None

        self.game_state: GameState = GameState(**json_data)
        self.current_level: Level = Level(self)
        self.text_rendering: TextRendering = TextRendering()
        self.screen_manager: ScreenManager = ScreenManager(
            self, self.current_level)
        self.state_to_call: Callable[[], None] = \
            self.screen_manager.launch_game.display_screen

    def launch(self) -> None:
        frame_time_elapse: float = 0.0

        while self.active:
            start_time = time.monotonic()

            self.event_manager()
            if not self.active:
                pygame.quit()
                break

            if frame_time_elapse > self.frame_time:
                frame_time_elapse -= self.frame_time
                self.frame_count += 1

            if self.frame_count == 60:
                self.frame_count = 0

            self.state_to_call()
            self.display_on_screen()
            self.reset_event()

            frame_time_elapse += time.monotonic() - start_time

    @staticmethod
    def mlx_get_screen_size() -> tuple[int, int]:
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def _adjust_screen_size(self) -> pygame.Surface:
        """Resize the pygame window so it fits within the physical display."""
        screen_width, screen_height = self.mlx_get_screen_size()

        self.screen_height = screen_height
        self.screen_width = screen_width

        return pygame.display.set_mode((screen_width, screen_height))

    def clear_last_frame(self, color: str = "black") -> None:  # useless ?
        """Clear the last frame, recover it with a screen with a color"""
        self.screen.fill(pygame.Color(color))

    @staticmethod
    def display_on_screen() -> None:
        """Display everything that you prepared to the screen"""
        pygame.display.flip()

    def event_manager(self) -> None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.active = False
                break

            if event.type == pygame.KEYDOWN:
                self.key_pressed = event.unicode
                if event.key == pygame.K_ESCAPE:
                    self.state_to_call = (
                        self.screen_manager.pause_menu.display_screen)

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

        function_to_call = self._get_matching_screen()
        function_to_call.screen_selector(events)

    def _get_matching_screen(self) -> Any:
        screens = (
            self.screen_manager.game_play,
            self.screen_manager.main_menu,
            self.screen_manager.pause_menu,
            self.screen_manager.game_over,
            self.screen_manager.victory,
            self.screen_manager.instructions,
            self.screen_manager.leaderboard,
            self.screen_manager.launch_game
        )
        return next(
            (screen for screen in screens
             if self.state_to_call == screen.display_screen))

    def reset_event(self) -> None:
        self.key_pressed = None
        self.mouse_click = None
        self.delete_pressed = False
