from .screen import Screen


class LeaderBoard(Screen):
    def __init__(self) -> None:
        self.scores: dict[int, int] = {}
        self.names: dict[int, str] = {}
        self._init_score()

    def display_leaderboard(self) -> None:  # TODO
        pass

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

    def display_screen(self) -> None:  # TODO
        pass

    def event_manager(self) -> None:  # TODO
        pass


if __name__ == "__main__":
    leaderboard = LeaderBoard()
    print(f"{leaderboard.scores}: {leaderboard.names}")
    leaderboard.update_leaderboard(1, 3000, "yohan")
    leaderboard.add_new_highscore(10000, "nico")
    print(f"{leaderboard.scores}: {leaderboard.names}")
