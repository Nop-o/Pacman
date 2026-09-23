from . import Pacgum
import pygame
from ..entity import Character
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visual_simulation import SimulationManager


class SuperPacgum(Pacgum):
    """A collectible super pacgum that lets Pac-Man hunt ghosts temporarily."""

    def __init__(self, line_pos: int, column_pos: int) -> None:
        """Initialize the super pacgum's position and sprite.

        Args:
            line_pos: Line position of the super pacgum in the maze.
            column_pos: Column position of the super pacgum in the maze.
        """
        super().__init__(line_pos, column_pos)
        path = self.resource_path("png/entities_sprite.png")
        self.sprite: pygame.Surface = self.get_sprite(
            path, 401, 454, 35, 35)

    def eat(self, simulation_manager: "SimulationManager") -> None:
        """Award points, start the effect cooldown, and set ghosts to hunting.

        Args:
            simulation_manager: The simulation manager holding the game state
                and level.
        """
        game_state = simulation_manager.game_state
        level = simulation_manager.screen_manager.game_play.level
        game_state.score += game_state.points_per_super_pacgum
        level.super_pacgum_cooldown = time.monotonic() +\
            game_state.super_pacgum_cooldown
        level.change_state(Character.State.HUNTING)
