from . import Screen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager, TextRendering


class HUD(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.text_rendering: TextRendering =\
            self.simulation_manager.text_rendering

    def show_score(self) -> None:
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

    def show_lives(self) -> None:
        game_play = self.simulation_manager.screen_manager.game_play
        pacman_sprite = game_play.level.pacman.sprites[0][1]
        level = self.simulation_manager.screen_manager.game_play.level
        lives_position = (
            level.MAZE_START[0] + 20,
            level.MAZE_END[1] + 20
        )
        offset = pacman_sprite.get_width() + 10
        for i in range(self.simulation_manager.game_state.current_lives):
            pos = (lives_position[0] + (offset * i), lives_position[1])
            self.simulation_manager.screen.blit(
                source=pacman_sprite,
                dest=pos
            )
        

    def show_level(self) -> None:  # TODO
        level = self.simulation_manager.screen_manager.game_play.level
        level_nb = self.text_rendering.render_regular_text(
            f"Level {self.simulation_manager.game_state.nb_level}",
            (255, 255, 255)
            )
        level_pos = (
            level.MAZE_END[0] - 20 - level_nb.get_width(),
            level.MAZE_END[1] + 20
            )
        self.simulation_manager.screen.blit(
            source=level_nb,
            dest=level_pos
        )
        

    def show_timer(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:
        self.show_score()
        self.show_lives()
        self.show_level()
        self.show_timer()
