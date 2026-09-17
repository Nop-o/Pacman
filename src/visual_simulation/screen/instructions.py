from . import Screen, Level
from typing import TYPE_CHECKING
import pygame
from ...entity import Character

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Instructions(Screen):
    """Instructions screen explaining the game's rules and controls."""

    def __init__(self, simulation_manager: "SimulationManager") -> None:
        """Initialize the instructions screen's direction state and sprites.

        Args:
            simulation_manager: The simulation manager driving the game.
        """
        super().__init__(simulation_manager=simulation_manager)

        self.current_direction: Character.FacingDirection = \
            Character.FacingDirection.RIGHT

        self.arcade_pacman_sprite: pygame.Surface = \
            self.simulation_manager.get_sprite(
                "png/arcade_pacman.png", 50, 10, 380, 475)

        self.running_pacman_sprite: pygame.Surface = \
            self.simulation_manager.get_sprite(
                "png/running_pacman_small.png", 10, 0, 360, 335)

        self.small_pacman_logo_sprite: pygame.Surface = \
            self.simulation_manager.get_sprite(
                "png/small_pacman_logo.png", 10, 120, 295, 75)

    def display_instruction_titles(self, screen: pygame.Surface,
                                   screen_titles: list[pygame.Surface]
                                   ) -> None:
        """Draw the instruction titles and the demo entities below them.

        Args:
            screen: Surface to draw on.
            screen_titles: Rendered text surfaces, the main title followed
                by each instruction line.
        """
        main_title_padding: int = self.simulation_manager.screen_height // 10
        text_y_padding: int = \
            main_title_padding + screen_titles[0].get_height() + 30
        text_x_padding: int = int(self.simulation_manager.screen_width // 3.2)

        screen.blit(screen_titles[0], (
            self.get_center_width(screen_titles[0]), main_title_padding))

        for i in range(1, len(screen_titles), 1):
            screen.blit(screen_titles[i], (
                text_x_padding,
                text_y_padding + ((
                    self.simulation_manager.screen_height // 15) * i)))

        pacman_x: int = text_x_padding + screen_titles[1].get_width() + 50
        pacman_y: int = \
            text_y_padding + self.simulation_manager.screen_height // 15
        ghost_x: int = self.simulation_manager.screen_width // 2 - 100
        ghost_y: int = text_y_padding + ((
            self.simulation_manager.screen_height // 15) * (i + 1))

        self.display_entities((pacman_x, pacman_y), ghost_x, ghost_y)

    def display_entities(self, pacman_position: tuple[int, int],
                         x_padding: int, y_padding: int) -> None:
        """Draw demo sprites of the ghosts and Pac-Man on the instructions screen.

        Args:
            pacman_position: Position to draw the Pac-Man sprite at.
            x_padding: Starting horizontal position for the ghost sprites.
            y_padding: Vertical position for the ghost sprites.
        """
        level: Level = self.simulation_manager.screen_manager.game_play.level

        for i, ghost in enumerate(level.ghosts, 0):
            sprites = getattr(ghost, "sprites")

            self.simulation_manager.screen.blit(
                sprites[self.current_direction][
                    self.simulation_manager.frame_count % 2],
                (x_padding + (50 * i), y_padding))

        self.simulation_manager.screen.blit(level.pacman.sprites[
            self.current_direction][self.simulation_manager.frame_count % 3],
            pacman_position)

    def display_screen(self) -> None:
        """Render the instructions screen, its titles, and decorative sprites."""
        self.simulation_manager.dipslay_sky()

        screen_titles: list[pygame.Surface] = [
            self.simulation_manager.text_rendering.render_big_title(
                "Instructions", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "You are a Pacman.", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "Your mission is to eat all of the pacgum.", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "But be careful !!", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "Shadow, Speedy, Bashful and Pokey will let not you do it "
                "easily.", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "To help you, there will be some superpacgum.", (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "They will make you invincible and them edible.",
                (255, 255, 0)),
            self.simulation_manager.text_rendering.render_regular_text(
                "Good luck and have fun !", (255, 255, 0)),
        ]

        self.simulation_manager.screen.blit(
            self.arcade_pacman_sprite,
            (70, self.simulation_manager.screen_height - 620))
        self.simulation_manager.screen.blit(
            self.running_pacman_sprite,
            (self.simulation_manager.screen_width - 400, 70))
        self.simulation_manager.screen.blit(
            self.small_pacman_logo_sprite,
            (self.simulation_manager.screen_width - 350,
             self.simulation_manager.screen_height - 200))

        self.display_instruction_titles(
            self.simulation_manager.screen, screen_titles)

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        """Handle input events for navigation and changing the demo direction.

        Args:
            events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    self.main_menu_screen()
                    return

                if event.key == pygame.K_LEFT:
                    self.current_direction = \
                        Character.FacingDirection.LEFT
                if event.key == pygame.K_RIGHT:
                    self.current_direction = \
                        Character.FacingDirection.RIGHT
                if event.key == pygame.K_DOWN:
                    self.current_direction = \
                        Character.FacingDirection.DOWN
                if event.key == pygame.K_UP:
                    self.current_direction = \
                        Character.FacingDirection.UP
