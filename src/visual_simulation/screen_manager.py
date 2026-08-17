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
        self.victory: Victory = victory


if __name__ == "__main__":
    from .. import GameState
    from ..entity import Pacman, Ghost
    from ...maze import Maze
    from ...algorithm import DepthFirstSearch

    maze = Maze()
    algo = DepthFirstSearch(entry=(1, 1), exit=(1, 2), maze=maze)
    pacman = Pacman(lives=10, maze=maze, super_pacgum_cooldown=10)

    ghost_1 = Bashful(
        maze=maze,pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
    ghost_2 = Shadow(
        maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
    ghost_3 = Speedy(
        maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)
    ghost_4 = Pokey(
        maze=maze, pacman=pacman, super_pacgum_cooldown=10, algorithm=algo)

    game_state = GameState(pacgum=10, points_per_pacgum=100,
                           points_per_super_pacgum=10, super_pacgum_time=10,
                           points_per_ghost=1000, seed=42, level_max_time=200,
                           pacman=pacman, ghosts=[ghost_1, ghost_2, ghost_3, ghost_4])
    level = Level(game_state)

    sceen_manager = ScreenManager(game_state=game_state, level=level)
