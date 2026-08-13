from .leaderboard import LeaderBoard
from .screen import Screen


class Victory(Screen):
    def __init__(self, score: int, leaderboard: LeaderBoard) -> None:
        self.score: int = score

    def display_screen(self) -> None:  # TODO
        pass
