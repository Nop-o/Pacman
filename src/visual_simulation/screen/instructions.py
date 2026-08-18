from . import Screen
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Instructions(Screen):
    def __init__(self, simulation_manager: "SimulationManager",
                 font: pygame.font.Font = pygame.font.Font(None, 80),
                 big_font: pygame.font.Font = pygame.font.Font(None, 30)
                 ) -> None:
        super().__init__(
            simulation_manager=simulation_manager,
            font=font, big_font=big_font)

    def display_screen(self) -> None:  # TODO
        pass

    def event_manager(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.go_to_main_menu()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.go_to_main_menu()
                    return
