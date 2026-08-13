from .main_menu import MainMenu
from .game_play import GamePlay
from .screen import Screen


class PauseMenu(Screen):
    def __init__(self, main_menu: MainMenu, game_play: GamePlay) -> None:
        self.main_menu = main_menu
        self.game_play = game_play

    def resume_game(self) -> None:  #  TODO
        pass

    def return_to_main_menu() -> None:  # TODO
        pass

    def display_screen(self) -> None:  # TODO
        pass
