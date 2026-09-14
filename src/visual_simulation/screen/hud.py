from . import Screen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager, TextRendering


class HUD(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.text_rendering: TextRendering =\
            self.simulation_manager.text_rendering

    def show_score(self) -> None:  # TODO
        title_score = self.text_rendering.render_small_title(
            "Score", (255, 255, 255))
        title_score_pos = (
            self.simulation_manager.screen_width // 2 -
            title_score.get_width() // 2,
            50
        )
        score_text = self.text_rendering.render_small_title(
            f"{self.simulation_manager.game_state.score}",
            (255, 255, 255))
        score_text_pos = (
            self.simulation_manager.screen_width // 2 -
            score_text.get_width() // 2,
            50 + title_score.get_height() + 10
        )
        self.simulation_manager.screen.blit(
            title_score,
            title_score_pos
        )
        self.simulation_manager.screen.blit(
            score_text,
            score_text_pos
        )

    def show_lives(self) -> None:  # TODO
        pass

    def show_level(self) -> None:  # TODO
        pass

    def show_timer(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:
        self.show_score()
        self.show_lives()
        self.show_level()
        self.show_timer()
