from ...game_state import GameState

class HUD():
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def show_score(self):
        pass

    def show_lives(self):
        pass

    def show_level(self):
        pass

    def show_timer(self):
        pass