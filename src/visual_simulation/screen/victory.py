from .leaderboard import LeaderBoard


class Victory:
    def __init__(self, score: int, leaderboard: LeaderBoard) -> None:
        self.score: int = score
