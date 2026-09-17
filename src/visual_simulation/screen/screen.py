from abc import ABC, abstractmethod
import pygame
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Screen(ABC):
    """Abstract base class for all game screens, with shared UI helpers."""

    def __init__(self, simulation_manager: "SimulationManager") -> None:
        """Store a reference to the simulation manager driving the game.

        Args:
            simulation_manager: The simulation manager driving the game.
        """
        self.simulation_manager: "SimulationManager" = simulation_manager

    @abstractmethod
    def display_screen(self) -> None:
        """Render this screen's current frame."""
        ...

    def main_menu_screen(self) -> None:
        """Switch the active screen to the main menu."""
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.main_menu.display_screen

    def victory_screen(self) -> None:
        """Switch the active screen to the victory screen, resetting its input.
        """
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.victory.display_screen
        self.simulation_manager.screen_manager.victory.user_name = ""

    def game_over_screen(self) -> None:
        """Switch the active screen to the game over screen, resetting its
        input."""
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_over.display_screen
        self.simulation_manager.screen_manager.game_over.user_name = ""

    def game_play_screen(self) -> None:
        """Switch the active screen to gameplay, resetting the level's timers.
        """
        self.simulation_manager.screen_manager.game_play.level.reset_timer()
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.game_play.display_screen

    def leaderboard_screen(self) -> None:
        """Switch the active screen to the leaderboard."""
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.leaderboard.display_screen

    def pause_screen(self) -> None:
        """Switch the active screen to the pause menu."""
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.pause_menu.display_screen

    def instructions_screen(self) -> None:
        """Switch the active screen to the instructions screen."""
        self.simulation_manager.state_to_call = \
            self.simulation_manager.screen_manager.instructions.display_screen

    def exit_game(self) -> None:
        """Stop the simulation loop, exiting the game."""
        self.simulation_manager.active = False

    def new_game(self) -> None:
        """Start a fresh game with a new level and reset game state."""
        from . import Level
        self.simulation_manager.screen_manager.game_play.level =\
            Level(self.simulation_manager)
        self.simulation_manager.game_state.reset_game_state()
        self.game_play_screen()

    def next_level(self) -> None:
        """Advance to the next level, or go to the victory screen if finished.
        """
        from . import Level
        if self.simulation_manager.game_state.nb_level + 1 >= 11:
            self.victory_screen()
            return
        self.simulation_manager.game_state.seed += 1
        self.simulation_manager.game_state.nb_level += 1
        self.simulation_manager.game_state.is_game_won = False
        self.simulation_manager.screen_manager.game_play.level =\
            Level(self.simulation_manager)

    def make_button(self,
                    pos: tuple[int, int],
                    text: pygame.Surface,
                    action: Callable[[], None],
                    px: int,
                    py: int) -> None:
        """Draw a clickable button and trigger an action if clicked.

        Args:
            pos: The (x, y) position of the button's top center.
            text: The rendered text to display on the button.
            action: The callback to invoke when the button is clicked.
            px: Horizontal padding added to the text width.
            py: Vertical padding added to the text height.
        """
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
        """Draw text centered on screen, with an optional offset.

        Args:
            text: The rendered text surface to draw.
            width_adjust: Horizontal offset from the centered position.
            height_adjust: Vertical offset from the centered position.
        """
        x, y = self.get_text_pos(
            text, width_adjust=width_adjust, height_adjust=height_adjust)

        self.simulation_manager.screen.blit(text, (x, y))

    def get_text_pos(self, text: pygame.Surface,
                     width_adjust: int = 0,
                     height_adjust: int = 0) -> tuple[int, int]:
        """Compute the position to center text on screen, with an offset.

        Args:
            text: The rendered text surface to position.
            width_adjust: Horizontal offset from the centered position.
            height_adjust: Vertical offset from the centered position.

        Returns:
            The (x, y) position to draw the text at.
        """
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
        """Draw a filled rectangle pixel by pixel.

        Args:
            coord: The (x, y) position of the rectangle's origin.
            width: Width of the rectangle in pixels.
            height: Height of the rectangle in pixels.
            color: RGB color of the rectangle.
            center_width: Whether to center the rectangle horizontally on coord
            center_height: Whether to center the rectangle vertically on coord.
        """
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

    def display_titles(
       self, screen: pygame.Surface, titles: list[pygame.Surface],
       title_padding: list[int]) -> None:
        """Draw a list of titles, each centered horizontally at its padding.

        Args:
            screen: Surface to draw on.
            titles: Rendered title surfaces to draw.
            title_padding: Vertical position for each title.
        """
        for i, title in enumerate(titles, 0):
            screen.blit(
                title, (self.get_center_width(title), title_padding[i]))

    def get_title_paddings(
       self, texts: list[pygame.Surface], main_title_padding_size: int,
       title_padding_size: int) -> list[int]:
        """Compute the vertical position for a main title and subsequent
        titles.

        Args:
            texts: The list of title surfaces to position.
            main_title_padding_size: Divisor of the screen height giving the
                main title's vertical position.
            title_padding_size: Divisor of the screen height giving the
                spacing between subsequent titles.

        Returns:
            The vertical position for each title, in order.
        """
        main_title_padding: int = \
            self.simulation_manager.screen_height // main_title_padding_size
        title_padding: int = \
            self.simulation_manager.screen_height // title_padding_size
        return_value: list[int] = []

        for i in range(len(texts)):
            return_value.append(int(main_title_padding + (title_padding * i)))

        return return_value

    def get_center_width(self, surface: pygame.Surface) -> int:
        """Compute the horizontal position to center a surface on screen.

        Args:
            surface: The surface to center.

        Returns:
            The x position to draw the surface at.
        """
        return ((self.simulation_manager.screen_width // 2) -
                (surface.get_width() // 2))

    def add_two_tuple(self, tuple_1: tuple[int, int],
                      tuple_2: tuple[int, int]) -> tuple[int, int]:
        """Add two (x, y) tuples element-wise.

        Args:
            tuple_1: The first tuple.
            tuple_2: The second tuple.

        Returns:
            The element-wise sum of the two tuples.
        """
        x_1, y_1, = tuple_1
        x_2, y_2, = tuple_2

        return (x_1 + x_2, y_1 + y_2)

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
