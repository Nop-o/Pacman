from . import Screen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class HUD(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)

    def show_score(self) -> None:  # TODO
        pass

    def show_lives(self) -> None:  # TODO
        pass

    def show_level(self) -> None:  # TODO
        pass

    def show_timer(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:
        self.simulation_manager.screen.fill((0, 0, 0))
        self.show_score()
        self.show_lives()
        self.show_level()
        self.show_timer()
