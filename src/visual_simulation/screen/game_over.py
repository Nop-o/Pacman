from .screen import Screen
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GameOver(Screen):
    """Game over screen, offering highscore entry or a return to the menu."""

    def __init__(self, simulation_manager: "SimulationManager") -> None:
        """Initialize the game over screen's user input and logo sprite.

        Args:
            simulation_manager: The simulation manager driving the game.
        """
        super().__init__(simulation_manager=simulation_manager)
        self.user_name = ""
        self.pacman_logo: pygame.Surface = self.get_sprite(
            "png/pacman_logo_small.png", 10, 0, 640, 380)

    def display_screen(self) -> None:
        """Render the game over screen, prompting for a name if applicable."""
        self.simulation_manager.dipslay_sky()

        game_over_text = \
            self.simulation_manager.text_rendering.render_small_title(
                "GAME OVER", (255, 255, 255))

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

            button_pos = (
                self.simulation_manager.screen_width // 2,
                self.simulation_manager.screen_height // 2 + 175
            )
            self.make_button(
                button_pos, button_text, self.button_action, 50, 20)

        else:
            text_prompt = \
                self.simulation_manager.text_rendering.render_regular_text(
                    "Press RETURN to go back to main menu ...", (255, 255, 255)
                    )

        self.draw_text(game_over_text, width_adjust=0, height_adjust=-100)
        self.draw_text(text_prompt, width_adjust=0, height_adjust=50)
        self.draw_sprites()

    def button_action(self) -> None:
        """Save the current score to the leaderboard and go to the leaderboard
        screen."""
        self.simulation_manager.screen_manager.leaderboard.add_new_highscore(
            self.simulation_manager.game_state.score, self.user_name)
        self.leaderboard_screen()

    def is_score_in_leaderboard(self) -> bool:
        """Check whether the current score qualifies for the leaderboard.

        Returns:
            True if the score beats the lowest leaderboard entry, False
            otherwise.
        """
        return (
            self.simulation_manager.game_state.score >
            self.simulation_manager.screen_manager.leaderboard.scores[9])

    def handle_user_writing(self) -> None:
        """Update the entered user name from the current key press or
        deletion."""
        if self.simulation_manager.key_pressed is not None:
            if self.simulation_manager.key_pressed.isprintable():
                if len(self.user_name) < 10:
                    self.user_name += self.simulation_manager.key_pressed
            if self.simulation_manager.delete_pressed is True:
                self.user_name = self.user_name[0:-1]

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        """Handle input events, exiting the game or returning to the main menu.

        Args:
            events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main_menu_screen()
                    return

    def draw_sprites(self) -> None:
        """Draw the Pac-Man logo centered near the top of the screen."""
        pos = (
            self.simulation_manager.screen_width // 2 -
            self.pacman_logo.get_width() // 2,
            50
        )
        self.simulation_manager.screen.blit(
            self.pacman_logo,
            pos
        )
