from .screen import Screen
from .hud import HUD
from .level import Level
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class GamePlay(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 level: Level, hud: HUD,
                 font: pygame.font.Font | None = None,
                 big_font: pygame.font.Font | None = None
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)
        self.level: Level = level
        self.hud: HUD = hud

    def display_screen(self) -> None:
        if self.simulation_manager.game_state.is_game_over:
            self.game_over_screen()
        if self.simulation_manager.game_state.is_game_won:
            self.victory_screen()

        self.level.display_screen()
        self.hud.display_screen()

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_screen()
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.simulation_manager.game_state.pacman.go_left()
                elif event.key [pygame.K_RIGHT, pygame.K_d]:
                    self.simulation_manager.game_state.pacman.go_right()
                elif event.key [pygame.K_UP, pygame.K_w]:
                    self.simulation_manager.game_state.pacman.go_up()
                elif event.key [pygame.K_DOWN, pygame.K_s]:
                    self.simulation_manager.game_state.pacman.go_down()
