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
        self.game_over: GameOver = game_over
        self.game_play: GamePlay = game_play
        self.hud: HUD = hud
        self.leaderboard: LeaderBoard = leaderboard
        self.main_menu: MainMenu = main_menu
        self.pause_menu: PauseMenu = pause_menu
        self.victory: Victory = victory
