class ScoreBoard:
    def __init__(self) -> None:
        self.scoreboard : dict[tuple[str, int]] = self._init_score()

    def _init_score(self) -> dict[tuple[str, int]]:
        """Initialize the scoreboard"""
        scoreboard: dict[tuple[str, int]]

        for i in range(1, 10, 1):
            scoreboard[i] = ("", 0)
        return scoreboard
