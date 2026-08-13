from .game_play import GamePlay
from .leaderboard import LeaderBoard
from .screen import Screen


class MainMenu(Screen):
    def __init__(self, game_play: GamePlay, leaderboard: LeaderBoard) -> None:
        self.game_play: GamePlay = GamePlay
        self.leaderboard: leaderboard = LeaderBoard

    def exit_game(self) -> None:  # TODO
        pass

    def start_game(self) -> None:  # TODO
        pass

    def show_instructions(self) -> None:  # TODO
        pass

    def view_leaderboard(self) -> None:  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        pass
