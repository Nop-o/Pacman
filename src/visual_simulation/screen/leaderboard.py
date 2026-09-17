from . import Screen
from typing import TYPE_CHECKING
import pygame
import json

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class LeaderBoard(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.scores: dict[int, int] = {}
        self.names: dict[int, str] = {}
        self._import_highscore()

    def _init_score(self) -> None:
        """Initialize the leaderboard"""
        for i in range(1, 11, 1):
            self.scores[i] = 0
            self.names[i] = ""

    def add_new_highscore(self, score: int, name: str) -> None:
        """Try to update the leaderboard with a new score"""
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
        """Update score/name in the leaderboard"""
        self.scores[position] = score
        self.names[position] = name

    def _is_score_in_top_10(self, score: int) -> bool:
        """Verify if a new score can be in the leaderboard"""
        return score > self.scores[10]

    def _get_score_position(self, score: int) -> int:
        """Get the position in the leaderboard of a new score"""
        for i in range(1, 11, 1):
            if score > self.scores[i]:
                return i
        return -1

    def display_screen(self) -> None:
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
        screen: pygame.Surface = self.simulation_manager.screen
        starting_width: int = self.simulation_manager.screen_width // 3
        padding_width: int = self.simulation_manager.screen_width // 7
        starting_height: int = self.simulation_manager.screen_height // 4
        padding_height: int = self.simulation_manager.screen_height // 18

        for i in range(1, 11, 1):
            screen.blit((
                self.simulation_manager.text_rendering.render_small_title(
                    f"{i}.", (255, 255, 0))),
                (starting_width, starting_height + (padding_height * i))
                )

        for i in range(1, 11, 1):
            screen.blit((
                self.simulation_manager.text_rendering.render_small_title(
                    f"{self.names[i]}", (255, 255, 0))),
                (starting_width + padding_width,
                 starting_height + (padding_height * i))
                    )

        for i in range(1, 11, 1):
            screen.blit((
                self.simulation_manager.text_rendering.render_small_title(
                    f"{self.scores[i]}", (255, 255, 0))),
                (starting_width + (padding_width * 2.5),
                 starting_height + (padding_height * i))
                    )

    def export_highscore(self) -> None:
        with open("scores/highscore.json", "w") as file:
            file.write(json.dumps(self.scores))
        with open("scores/highscore_name.json", "w") as file:
            file.write(json.dumps(self.names))

    def _import_highscore(self) -> None:
        try:
            with open("scores/highscore.json", "r") as file:
                raw_scores = json.loads(file.read())
                self.scores = {int(k): v for k, v in raw_scores.items()}
            with open("scores/highscore_name.json", "r") as file:
                raw_names = json.loads(file.read())
                self.names = {int(k): v for k, v in raw_names.items()}
        except FileNotFoundError:
            self._init_score()

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                    self.simulation_manager.game_state.reset_game_state()
                    self.main_menu_screen()
                    return
