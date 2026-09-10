from . import Pacgum
import pygame
from ..entity import Character
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visual_simulation import SimulationManager


class SuperPacgum(Pacgum):
    def __init__(self, line_pos: int, column_pos: int) -> None:
        super().__init__(line_pos, column_pos)

        self.sprite: pygame.Surface = self.get_sprite(
            "png/entities_sprite.png", 401, 454, 35, 35)

    def eat(self, simulation_manager: "SimulationManager"):
        game_state = simulation_manager.game_state
        level = simulation_manager.screen_manager.game_play.level
        game_state.score += game_state.points_per_super_pacgum
        level.change_state(Character.State.HUNTING)
        level.super_pacgum_cooldown = time.monotonic() +\
            game_state.super_pacgum_cooldown
