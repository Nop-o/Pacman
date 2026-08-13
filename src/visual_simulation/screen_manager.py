from .screen.game_over import GameOver
from .screen.game_play import GamePlay
from .screen.hud import HUD
from .screen.leaderboard import LeaderBoard
from .screen.main_menu import MainMenu
from .screen.pause_menu import PauseMenu
from .screen.victory import Victory


class ScreenManager:
    def __init__(self, game_over: GameOver, game_play: GamePlay, hud: HUD,
                 leaderboard: LeaderBoard, main_menu: MainMenu,
                 pause_menu: PauseMenu, victory: Victory) -> None:
        self.game_over = game_over
        self.game_play = game_play
        self.hud = hud
        self.leaderboard = leaderboard
        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.victory = victory
