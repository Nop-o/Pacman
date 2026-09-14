from .screen import Screen
from .hud import HUD
from .level import Level
from typing import TYPE_CHECKING
import pygame
from ...entity import Character

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GamePlay(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 level: Level, hud: HUD,
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.level: Level = level
        self.hud: HUD = hud

    def display_screen(self) -> None:
        if self.simulation_manager.game_state.is_game_over is True:
            self.game_over_screen()

        elif self.simulation_manager.game_state.is_game_won is True:
            self.victory_screen()

        self.simulation_manager.dipslay_sky()

        self.level.display_screen()
        self.hud.display_screen()
        self.simulation_manager.button_manager.display_joystick(
        self.simulation_manager.screen, self.level.pacman.direction)

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_screen()

                if event.key == pygame.K_UP:
                    self.level.pacman.direction =\
                        Character.FacingDirection.UP
                if event.key == pygame.K_RIGHT:
                    self.level.pacman.direction =\
                        Character.FacingDirection.RIGHT
                if event.key == pygame.K_DOWN:
                    self.level.pacman.direction =\
                        Character.FacingDirection.DOWN
                if event.key == pygame.K_LEFT:
                    self.level.pacman.direction =\
                        Character.FacingDirection.LEFT
