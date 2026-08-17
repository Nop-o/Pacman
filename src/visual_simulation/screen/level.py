from ..simulation_manager import SimulationManager
from ...entity import Ghost, Pacman, Pokey, Shadow, Speedy, Bashful
from ...maze import Maze
from . import Screen


class Level(Screen):
    def __init__(self, simulation_manager: SimulationManager,
                 seed: int = 0) -> None:

        # need fill ghosts and pacman
        self.maze = Maze(seed=seed)
        self.simulation_manager: SimulationManager = SimulationManager
        self.ghosts: list[Ghost] = [
            Pokey(
                self.maze, self.simulation_manager.game_state.pacman,
                self.simulation_manager.game_state.super_pacgum_cooldown,
                self.simulation_manager.game_state.algorithm),
            Bashful(
                self.maze, self.simulation_manager.game_state.pacman,
                self.simulation_manager.game_state.super_pacgum_cooldown,
                self.simulation_manager.game_state.algorithm),
            Speedy(
                self.maze, self.simulation_manager.game_state.pacman,
                self.simulation_manager.game_state.super_pacgum_cooldown,
                self.simulation_manager.game_state.algorithm),
            Shadow(
                self.maze, self.simulation_manager.game_state.pacman,
                self.simulation_manager.game_state.super_pacgum_cooldown,
                self.simulation_manager.game_state.algorithm),
        ]
        # need pacgum, either in list with coord form or object

    # TODO Do the turn by calling in order move_pacman, move_ghost, load_maze,
    # load_pacgum, load_ghost and load_pacman
    def do_turn(self) -> None:
        pass

    # TODO move pacman according to the direection input
    def move_pacman(self) -> None:
        pass

    # TODO move the ghosts
    def move_ghosts(self) -> None:
        pass

    # TODO load in pygame the background and the wall of the maze
    def load_maze(self) -> None:
        pass

    # TODO load in pygame the pacgum
    def load_pacgum(self) -> None:
        pass

    # TODO load in pygame the ghosts
    def load_ghost(self) -> None:
        pass

    # TODO load in pygame pacman
    def load_pacman(self) -> None:
        pass

    # TODO remove a life, and if 0 remaining call lose_game function
    def lose_life(self) -> None:
        pass

    # TODO set the screen to losing menu
    def lose_game(self) -> None:
        pass

    # TODO set the screen to victory menu
    def win_game(self) -> None:
        pass

    def display_screen(self) -> bool:
        pass

    def event_manager(self) -> bool:  # TODO
        pass
