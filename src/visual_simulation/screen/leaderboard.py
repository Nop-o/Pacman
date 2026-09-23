from . import Screen
from typing import TYPE_CHECKING
import pygame
import json

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LeaderBoard(Screen):
    """Leaderboard screen showing and persisting the top 10 highscores."""

    def __init__(self, simulation_manager: "SimulationManager") -> None:
        """Initialize the leaderboard and load saved highscores.

        Args:
            simulation_manager: The simulation manager driving the game.
        """
        super().__init__(simulation_manager=simulation_manager)
        self.scores: dict[int, int] = {}
        self.names: dict[int, str] = {}
        self._import_highscore()

        self.leaderboard_error: bool = False

    def _init_score(self) -> None:
        """Initialize the leaderboard with empty scores and names."""
        for i in range(1, 11, 1):
            self.scores[i] = 0
            self.names[i] = ""

    def add_new_highscore(self, score: int, name: str) -> None:
        """Insert a new score into the leaderboard, shifting lower scores down.

        Args:
            score: The score to add.
            name: The name associated with the score.
        """
        if not self._is_score_in_top_10(score):
            return

        position: int = self._get_score_position(score)
        if position < 0:
            return
        old_scores = {i: self.scores[i] for i in range(position, 11)}
        old_names = {i: self.names[i] for i in range(position, 11)}

        self.update_leaderboard(position, score, name)

        for i in range(position + 1, 11):
            self.update_leaderboard(i, old_scores[i - 1], old_names[i - 1])

    def update_leaderboard(self, position: int, score: int, name: str) -> None:
        """Set the score and name at a given leaderboard position.

        Args:
            position: The leaderboard rank to update, from 1 to 10.
            score: The score to store at that position.
            name: The name to store at that position.
        """
        self.scores[position] = score
        self.names[position] = name

    def _is_score_in_top_10(self, score: int) -> bool:
        """Check whether a score qualifies for the top 10.

        Args:
            score: The score to check.

        Returns:
            True if the score beats the current 10th place, False otherwise.
        """
        return score > self.scores[10]

    def _get_score_position(self, score: int) -> int:
        """Find the leaderboard rank a new score should be inserted at.

        Args:
            score: The score to place.

        Returns:
            The rank from 1 to 10 the score should occupy, or -1 if it
            doesn't qualify.
        """
        for i in range(1, 11, 1):
            if score > self.scores[i]:
                return i
        return -1

    def display_screen(self) -> None:
        """Render the leaderboard screen, its title, and the highscores."""
        self.simulation_manager.dipslay_sky()

        leaderboard_text = \
            self.simulation_manager.text_rendering.render_big_title(
                "LeaderBoard", (255, 255, 0))

        self.simulation_manager.display_menu_sprites()

        self.simulation_manager.screen.blit(
            leaderboard_text, (self.get_center_width(leaderboard_text),
                               self.simulation_manager.screen_height // 10)
        )

        self.display_highscores()

    def display_highscores(self) -> None:
        """Draw the rank, name, and score of each leaderboard entry."""
        screen: pygame.Surface = self.simulation_manager.screen
        starting_width: int = self.simulation_manager.screen_width // 3
        padding_width: int = self.simulation_manager.screen_width // 7
        starting_height: int = int(
            self.simulation_manager.screen_height // 3.5)
        padding_height: int = self.simulation_manager.screen_height // 18

        position_text: pygame.Surface = \
            self.simulation_manager.text_rendering.render_small_title(
                "position".center(15), (255, 255, 0))
        name_text: pygame.Surface = \
            self.simulation_manager.text_rendering.render_small_title(
                "name".center(15), (255, 255, 0))
        score_text: pygame.Surface = \
            self.simulation_manager.text_rendering.render_small_title(
                "score".center(15), (255, 255, 0))

        screen.blit(
            position_text, (starting_width +
                            (padding_width - position_text.get_width()),
                            starting_height - 30))
        for i in range(1, 11, 1):
            try:
                screen.blit((
                    self.simulation_manager.text_rendering.render_small_title(
                        f"{i}.", (255, 255, 0))),
                    (starting_width, starting_height + (padding_height * i))
                    )
            except KeyError as e:
                if not self.leaderboard_error:
                    print(f"Missing key: missing leaderboard key {e}")
                    self.leaderboard_error = True

        screen.blit(
            name_text, (starting_width +
                        ((padding_width * 2) - name_text.get_width()),
                        starting_height - 30))
        for i in range(1, 11, 1):
            try:
                screen.blit((
                    self.simulation_manager.text_rendering.render_small_title(
                        f"{self.names[i][0:10]}", (255, 255, 0))),
                    (starting_width + padding_width,
                     starting_height + (padding_height * i))
                        )
            except KeyError as e:
                if not self.leaderboard_error:
                    print(f"Missing key: missing leaderboard key {e}")
                    self.leaderboard_error = True

        screen.blit(
            score_text, (starting_width +
                         ((padding_width * 3) - score_text.get_width()),
                         starting_height - 30))
        for i in range(1, 11, 1):
            try:
                screen.blit((
                    self.simulation_manager.text_rendering.render_small_title(
                        f"{self.scores[i]}", (255, 255, 0))),
                    (starting_width + (padding_width * 2.5),
                     starting_height + (padding_height * i))
                        )
            except KeyError as e:
                if not self.leaderboard_error:
                    print(f"Missing key: missing leaderboard key {e}")
                    self.leaderboard_error = True

    def export_highscore(self) -> None:
        """Save the current scores and names to their JSON files."""
        path_score = self.simulation_manager.persistent_data_path(
            "highscore.json")
        path_name = self.simulation_manager.persistent_data_path(
            "highscore_name.json"
        )
        with open(path_score, "w") as file:
            file.write(json.dumps(self.scores))
        with open(path_name, "w") as file:
            file.write(json.dumps(self.names))

    def _import_highscore(self) -> None:
        """Load scores and names from their JSON files, or initialize them."""
        path_score = self.simulation_manager.persistent_data_path(
            "highscore.json")
        path_name = self.simulation_manager.persistent_data_path(
            "highscore_name.json"
        )
        try:
            with open(path_score, "r") as file:
                raw_scores = json.loads(file.read())
                self.scores = {int(k): v for k, v in raw_scores.items()}
            with open(path_name, "r") as file:
                raw_names = json.loads(file.read())
                self.names = {int(k): v for k, v in raw_names.items()}
        except FileNotFoundError:
            self._init_score()

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        """Handle input events, exiting the game or returning to the main menu.

        Args:
            events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    self.simulation_manager.game_state.reset_game_state()
                    self.main_menu_screen()
                    return
