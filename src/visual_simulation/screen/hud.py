from ...game_state import GameState
from .screen import Screen


class HUD(Screen):
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def show_score(self):  # TODO
        pass

    def show_lives(self):  # TODO
        pass

    def show_level(self):  # TODO
        pass

    def show_timer(self):  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        pass
