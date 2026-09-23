from . import Entity
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visual_simulation import SimulationManager


class Pacgum(Entity):
    """A collectible pacgum placed at a fixed position in the maze."""

    def __init__(self, line_pos: int, column_pos: int) -> None:
        """Initialize the pacgum's position and sprite.

        Args:
            line_pos: Line position of the pacgum in the maze.
            column_pos: Column position of the pacgum in the maze.
        """
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        path = self.resource_path("png/entities_sprite.png")
        self.sprite: pygame.Surface = self.get_sprite(
            path, 401, 404, 35, 35)

    def eat(self, simulation_manager: "SimulationManager") -> None:
        """Award points for eating this pacgum.

        Args:
            simulation_manager: The simulation manager holding the game state.
        """
        game_state = simulation_manager.game_state
        game_state.score += game_state.points_per_super_pacgum
