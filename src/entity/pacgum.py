from . import Entity
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visual_simulation import SimulationManager


class Pacgum(Entity):

    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__()
        self.line_pos: int = line_pos
        self.column_pos: int = column_pos

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 404, 35, 35)

    def eat(self, simulation_manager: "SimulationManager"):
        game_state = simulation_manager.game_state
        game_state.score += game_state.points_per_super_pacgum
