import time
import pygame
from typing import Any, Callable
from .screen_manager import ScreenManager
from .text_rendering import TextRendering
from ..game_state import GameState
from ..entity import ButtonManager
from ..parsing import JsonData
import sys
import os


class SimulationManager():
    """Top-level driver managing the game loop, input, and screen state."""

    def __init__(self, json_data: JsonData) -> None:
        """Initialize pygame, the display, game state, and shared sprites.

        Args:
            json_data: Parsed configuration data for the game.
        """
        pygame.init()
        pygame.display.set_caption("Pac-Man")

        self.frame_count: int = 0
        self.frame_time: float = 0.8

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

        self.game_state: GameState = GameState(json_data)
        self.text_rendering: TextRendering = TextRendering()
        self.screen_manager: ScreenManager = ScreenManager(self)
        self.state_to_call: Callable[[], None] = \
            self.screen_manager.launch_game.display_screen

        self.sky: list[pygame.Surface] = [
            self.get_sprite(self.resource_path("png/bg_flat_1.png"),
                            0, 0, 1280, 720),
            self.get_sprite(self.resource_path("png/bg_flat_2.png"),
                            0, 0, 1280, 720),
            self.get_sprite(self.resource_path("png/bg_flat_3.png"),
                            0, 0, 1280, 720),
        ]

        self.button_manager: ButtonManager = ButtonManager(
            self.screen_width, self.screen_height)

        self.arcade_pacman_sprite: pygame.Surface = \
            self.get_sprite(self.resource_path("png/arcade_pacman.png"),
                            50, 10, 380, 475)

        self.running_pacman_sprite: pygame.Surface = \
            self.get_sprite(self.resource_path("png/running_pacman_small.png"),
                            10, 0, 360, 335)

    def dipslay_sky(self) -> None:
        """Tile the animated sky background across the entire screen."""
        width: int = 1280
        height: int = 720
        displayed_width: int = 0
        displayed_height: int = 0

        while displayed_height <= self.screen_height:
            while displayed_width <= self.screen_width:
                self.screen.blit(self.sky[self.frame_count % 3],
                                 (displayed_width, displayed_height))
                displayed_width += width
            displayed_height += height
            displayed_width = 0

    def launch(self) -> None:
        """Run the main game loop until the simulation is no longer active."""
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
        """Get the physical display's current resolution.

        Returns:
            The (width, height) of the display in pixels.
        """
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        """Extract a sprite region from a sprite sheet image.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.

        Returns:
            A surface containing the extracted sprite, with alpha channel.
        """
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image

    def _adjust_screen_size(self) -> pygame.Surface:
        """Resize the pygame window so it fits within the physical display.

        Returns:
            The created display surface.
        """
        screen_width, screen_height = self.mlx_get_screen_size()

        self.screen_height = screen_height
        self.screen_width = screen_width

        return pygame.display.set_mode((screen_width, screen_height))

    def clear_last_frame(self, color: str = "black") -> None:
        """Clear the last frame by filling the screen with a solid color.

        Args:
            color: The color to fill the screen with.
        """
        self.screen.fill(pygame.Color(color))

    @staticmethod
    def display_on_screen() -> None:
        """Flip the display buffer to show everything drawn this frame."""
        pygame.display.flip()

    def event_manager(self) -> None:
        """Process pygame events, updating input state and the active screen.
        """
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.active = False
                break

            if event.type == pygame.KEYDOWN:
                self.key_pressed = event.unicode

                if (event.key == pygame.K_DELETE or
                        event.key == pygame.K_BACKSPACE):
                    self.delete_pressed = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click = event.pos

        function_to_call = self._get_matching_screen()
        function_to_call.screen_selector(events)

    def _get_matching_screen(self) -> Any:
        """Find the screen instance whose display method is currently active.

        Returns:
            The currently active screen instance.
        """
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
        """Clear per-frame input state after it has been processed."""
        self.key_pressed = None
        self.mouse_click = None
        self.delete_pressed = False

    def display_menu_sprites(self) -> None:
        """Draw the decorative Pac-Man sprites shared across menu screens."""
        self.screen.blit(
            self.arcade_pacman_sprite, (70, self.screen_height - 620))
        self.screen.blit(
            self.running_pacman_sprite, (self.screen_width - 400, 70))

    @staticmethod
    def resource_path(relative_path: str) -> str:
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def persistent_data_path(filename: str) -> str:
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filename)
