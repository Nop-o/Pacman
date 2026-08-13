from .leaderboard import LeaderBoard
from .screen import Screen


class GameOver(Screen):
    def __init__(self, leaderboard: LeaderBoard) -> None:
        self.leaderboard: LeaderBoard = LeaderBoard

    def display_screen(self) -> None:  # TODO
        pass

    def event_manager(self) -> None:  # TODO
        pass
