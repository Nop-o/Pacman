from . import Screen, Level, HUD


class GamePlay(Screen):
    def __init__(self, level: Level, hud: HUD) -> None:
        self.level: Level = level
        self.hud: HUD = hud

    def display_screen(self) -> bool:
        self.level.display_screen()
        self.hud.display_screen()

    def event_manager(self) -> bool:  # TODO
        pass


if __name__ == "__main__":
    from ... import GameState
    from ...entity import Pacman
    from ...entity import Ghost
    from ...maze import Maze
    from ...algorithm import DepthFirstSearch

    maze = Maze()
    algo = DepthFirstSearch(entry=(1, 1), exit=(1, 2), maze=maze)
    pacman = Pacman(lives=10, maze=maze, super_pacgum_cooldown=10)

    ghost_1 = Ghost(maze=maze, starting_position=(10, 10), pacman=pacman,
                    super_pacgum_cooldown=10, algorithm=algo)
    ghost_2 = Ghost(maze=maze, starting_position=(11, 11), pacman=pacman,
                    super_pacgum_cooldown=10, algorithm=algo)

    game_state = GameState(pacgum=10, points_per_pacgum=100,
                           points_per_super_pacgum=10, super_pacgum_time=10,
                           points_per_ghost=1000, seed=42, level_max_time=200,
                           pacman=pacman, ghosts=[ghost_1, ghost_2])

    hud = HUD(game_state)
    level = Level(game_state)
    gameplay = GamePlay(level, hud)
