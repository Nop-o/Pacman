from ... import GameState


class HUD():
    def __init__(self, game_state: GameState) -> None:
        self.game_state = game_state

    def show_score(self) -> None:  # TODO
        pass

    def show_lives(self) -> None:  # TODO
        pass

    def show_level(self) -> None:  # TODO
        pass

    def show_timer(self) -> None:  # TODO
        pass

    def display_screen(self) -> bool:  # TODO
        pass
