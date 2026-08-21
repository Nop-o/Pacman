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
        test_message = \
            self.simulation_manager.text_rendering.render_small_title(
                "HUD", (255, 255, 255))

        test_message_pos = self.get_text_pos(test_message, height_adjust=-400)
        self.simulation_manager.screen.blit(test_message, test_message_pos)

        self.show_score()
        self.show_lives()
        self.show_level()
        self.show_timer()
