from .screen import Screen
from typing import TYPE_CHECKING
from ...maze import Direction
from ...entity.ghost import Ghost, Pacman

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Level(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:

        # TODO fix init -> pacman/ghost created here or before ?
        # need fill ghosts and pacman
        self.simulation_manager: SimulationManager = simulation_manager
        # need to fill ghost list
        self.ghosts: list[Ghost] = []
        # need to see what information pacman need
        self.pacman: Pacman
        # need pacgum, either in list with coord form or object

    # TODO Do the turn by calling in order move_pacman, move_ghost, load_maze,
    # load_pacgum, load_ghost and load_pacman
    def do_turn(self) -> None:
        pass

    # TODO move pacman according to the direection input
    def move_pacman(self) -> None:
        if self.simulation_manager.up_pressed:
            self.pacman.do_move(Direction.N)
        elif self.simulation_manager.right_pressed:
            self.pacman.do_move(Direction.E)
        elif self.simulation_manager.down_pressed:
            self.pacman.do_move(Direction.S)
        elif self.simulation_manager.left_pressed:
            self.pacman.do_move(Direction.W)
        else:
            self.pacman.do_move(None)

    # TODO move the ghosts
    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            ghost.get_goal()

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

    def display_screen(self) -> None:
        test_message = \
            self.simulation_manager.text_rendering.render_small_title(
                "level", (255, 255, 255))

        test_message_pos = self.get_text_pos(test_message, height_adjust=-200)
        self.simulation_manager.screen.blit(test_message, test_message_pos)
