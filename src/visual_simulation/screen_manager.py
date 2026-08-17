from .screen import (GameOver, GamePlay, HUD, LeaderBoard,
                     MainMenu, PauseMenu, Victory)
from .. import GameState


class ScreenManager:
    def __init__(self, game_state: GameState, level: Level) -> None:
        self.leaderboard: LeaderBoard = LeaderBoard()
        self.game_over: GameOver = GameOver(leaderboard=self.leaderboard)
        self.hud: HUD = HUD(game_state=game_state)

        self.game_play: GamePlay = GamePlay(level=level, hud=HUD)
        self.main_menu: MainMenu = main_menu()
        self.pause_menu: PauseMenu = pause_menu()
        self.victory: Victory = victory()
