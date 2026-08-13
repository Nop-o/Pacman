from .. import SimulationManager
from ...entity import Ghost, Pacman
from . import Screen

class Level(Screen):
    def __init__(self, simulation_manager: SimulationManager) -> None:
        self.simulation_manager: SimulationManager = simulation_manager
        # need fill ghosts and pacman
        self.ghosts: list[Ghost] = []
        self.pacman: Pacman
        # need pacgum, either in list with coord form or object

    # TODO Do the turn by calling in order move_pacman, move_ghost, load_maze,
    # load_pacgum, load_ghost and load_pacman
    def do_turn(self):
        pass

    # TODO move pacman according to the direection input
    def move_pacman(self):
        pass

    # TODO move the ghosts
    def move_ghosts(self):
        pass

    # TODO load in pygame the background and the wall of the maze
    def load_maze(self):
        pass

    # TODO load in pygame the pacgum
    def load_pacgum(self):
        pass

    # TODO load in pygame the ghosts
    def load_ghost(self):
        pass

    # TODO load in pygame pacman
    def load_pacman(self):
        pass

    # TODO remove a life, and if 0 remaining call lose_game function
    def lose_life(self):
        pass

    # TODO set the screen to losing menu
    def lose_game(self):
        pass

    # TODO set the screen to victory menu
    def win_game(self):
        pass

    def display_screen(self):
        pass

    def event_manager(self) -> None:  # TODO
        pass
