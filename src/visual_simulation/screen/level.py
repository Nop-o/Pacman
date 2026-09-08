from .screen import Screen
from typing import TYPE_CHECKING
from ...maze import Direction, Maze
from ...entity.ghost import Ghost, Pacman, Shadow, Speedy, Bashful, Pokey
from ...algorithm import DepthFirstSearch

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Level(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:

        # TODO fix init -> pacman/ghost created here or before ?
        # need fill ghosts and pacman
        self.simulation_manager: SimulationManager = simulation_manager
        self.maze: Maze = Maze(self.simulation_manager.game_state.seed)
        self.algo = DepthFirstSearch(self.maze)
        super_pacgum_cooldown =\
            self.simulation_manager.game_state.super_pacgum_cooldown
        self.pacman: Pacman =\
            Pacman(3, self.maze, super_pacgum_cooldown)
        self.ghosts: list[Ghost] = []
        self.ghosts.append(Shadow(self.maze, self.pacman,
                                  super_pacgum_cooldown, self.algo))
        self.ghosts.append(Speedy(self.maze, self.pacman,
                                  super_pacgum_cooldown, self.algo))
        self.ghosts.append(Bashful(self.maze, self.pacman,
                                   super_pacgum_cooldown, self.algo))
        self.ghosts.append(Pokey(self.maze, self.pacman,
                                 super_pacgum_cooldown, self.algo))
        # need pacgum, either in list with coord form or object
        self.CASE_SIZE = 50
        self.CASE_LINE_THICKNESS = 3

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

    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            ghost.do_turn()

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

    # TODO Do the turn by calling in order move_pacman, move_ghost, load_maze,
    # load_pacgum, load_ghost and load_pacman
    def display_screen(self) -> None:
        self.make_walls()

    def make_walls(self) -> None:
        for i, line in enumerate(self.maze.cases):
            for j, case in enumerate(line):
                if case.wall_north is True:
                    coord = (j * (self.CASE_SIZE + self.CASE_LINE_THICKNESS),
                             i * (self.CASE_SIZE + self.CASE_LINE_THICKNESS))
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_east is True:
                    coord = ((j + 1) *
                             (self.CASE_SIZE + self.CASE_LINE_THICKNESS),
                             i * (self.CASE_SIZE + self.CASE_LINE_THICKNESS))
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )
                if case.wall_south is True:
                    coord = (j * (self.CASE_SIZE + self.CASE_LINE_THICKNESS),
                             (i + 1) *
                             (self.CASE_SIZE + self.CASE_LINE_THICKNESS))
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_west is True:
                    coord = (j * (self.CASE_SIZE + self.CASE_LINE_THICKNESS),
                             i * (self.CASE_SIZE + self.CASE_LINE_THICKNESS))
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )
