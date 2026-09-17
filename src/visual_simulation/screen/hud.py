from . import Screen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import SimulationManager, TextRendering


class HUD(Screen):
    """Heads-up display showing score, lives, level, and timer."""

    def __init__(self, simulation_manager: "SimulationManager") -> None:
        """Initialize the HUD's text rendering reference.

        Args:
            simulation_manager: The simulation manager driving the game.
        """
        super().__init__(simulation_manager=simulation_manager)
        self.text_rendering: TextRendering =\
            self.simulation_manager.text_rendering

    def show_score(self) -> None:
        """Draw the current score and its title above the maze."""
        MAZE_START =\
            self.simulation_manager.screen_manager.game_play.level.MAZE_START
        score_text = self.text_rendering.render_regular_text(
            f"{self.simulation_manager.game_state.score}",
            (255, 255, 255))
        score_text_pos = (
            self.simulation_manager.screen_width // 2 -
            score_text.get_width() // 2,
            max(MAZE_START[1] - 10 - score_text.get_height(), 15)
        )
        title_score = self.text_rendering.render_small_title(
            "Score", (255, 255, 255))
        title_score_pos = (
            self.simulation_manager.screen_width // 2 -
            title_score.get_width() // 2,
            max(score_text_pos[1] - 5 - title_score.get_height(), 2)
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
        """Draw one Pac-Man sprite per remaining life, capped with an ellipsis."""
        game_play = self.simulation_manager.screen_manager.game_play
        pacman_sprite = game_play.level.pacman.sprites[0][1]
        level = self.simulation_manager.screen_manager.game_play.level
        lives_position = (
            level.MAZE_START[0] + 20,
            level.MAZE_END[1] + 20 + pacman_sprite.get_height() // 2
        )
        offset = pacman_sprite.get_width() + 10
        for i in range(self.simulation_manager.game_state.current_lives):
            pos = (lives_position[0] + (offset * i), lives_position[1])
            if i == 6:
                dot = self.text_rendering.render_regular_text(
                    "...", (255, 255, 255))
                pos = (
                    pos[0],
                    level.MAZE_END[1] + 20 + pacman_sprite.get_height() - 5
                )
                self.simulation_manager.screen.blit(
                    source=dot,
                    dest=pos
                )
                return
            self.simulation_manager.screen.blit(
                source=pacman_sprite,
                dest=pos
            )

    def show_level(self) -> None:
        """Draw the current level number below the maze."""
        level = self.simulation_manager.screen_manager.game_play.level
        level_nb = self.text_rendering.render_regular_text(
            f"Level {self.simulation_manager.game_state.nb_level}",
            (255, 255, 255)
        )
        level_pos = (
            level.MAZE_END[0] - 20 - level_nb.get_width(),
            level.MAZE_END[1] + 20 + level_nb.get_height() // 2
        )
        self.simulation_manager.screen.blit(
            source=level_nb,
            dest=level_pos
        )

    def show_timer(self) -> None:
        """Draw the remaining time for the current level below the maze."""
        level = self.simulation_manager.screen_manager.game_play.level
        game_state = self.simulation_manager.game_state
        timer_text = self.text_rendering.render_regular_text(
            f"{round(game_state.level_max_time - level.level_timer)}",
            (255, 255, 255)
        )
        timer_pos = (
            (level.MAZE_END[0] - level.MAZE_WIDTH // 2) -
            (timer_text.get_width() // 2),
            level.MAZE_END[1] + 20 + timer_text.get_height() // 2
        )
        self.simulation_manager.screen.blit(
            source=timer_text,
            dest=timer_pos
        )

    def display_screen(self) -> None:
        """Render all HUD elements: score, lives, level, and timer."""
        self.show_score()
        self.show_lives()
        self.show_level()
        self.show_timer()
