from .screen import Screen
from typing import TYPE_CHECKING
from ...maze import Direction, Maze
from ...entity.ghost import Ghost, Pacman, Shadow, Speedy, Bashful, Pokey
from ...algorithm import DepthFirstSearch
from ...entity import Entity, Pacgum, SuperPacgum, Character
import pygame
import random
import time

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Level(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:

        self.simulation_manager: SimulationManager = simulation_manager
        self.maze: Maze = Maze(self.simulation_manager.game_state.seed)
        self.algo = DepthFirstSearch(self.maze)
        super_pacgum_cooldown =\
            self.simulation_manager.game_state.super_pacgum_cooldown
        self.pacman: Pacman = Pacman(self.simulation_manager.game_state.lives,
                                     self.maze, super_pacgum_cooldown)
        self.ghosts: list[Ghost] = []
        # TODO need to fix speedy and bashfule chase algo, actually make crash
        self.ghosts.append(Shadow(self.maze, self.pacman,
                                  super_pacgum_cooldown, self.algo))
        # self.ghosts.append(Speedy(self.maze, self.pacman,
        #                           super_pacgum_cooldown, self.algo))
        # self.ghosts.append(Bashful(self.maze, self.pacman,
        #                            super_pacgum_cooldown, self.algo))
        self.ghosts.append(Pokey(self.maze, self.pacman,
                                 super_pacgum_cooldown, self.algo))
        self.pacgum: list[Pacgum] = []
        self.create_pacgums()
        self.CASE_SIZE = 55
        self.CASE_LINE_THICKNESS = 3
        self.MAZE_WIDTH = (self.CASE_SIZE) * self.maze.nb_column
        self.MAZE_HEIGHT = (self.CASE_SIZE) * self.maze.nb_line
        self.MAZE_START = (self.simulation_manager.screen_width // 2 -
                           self.MAZE_WIDTH // 2,
                           self.simulation_manager.screen_height // 2 -
                           self.MAZE_HEIGHT // 2 - 50
                           )
        self.lives: int = self.simulation_manager.game_state.lives
        self.super_pacgum_cooldown: float = 0

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

    def load_maze(self) -> None:
        for i, line in enumerate(self.maze.cases):
            for j, case in enumerate(line):
                if case.wall_north is True:
                    coord = ((j * self.CASE_SIZE) + self.MAZE_START[0],
                             (i * self.CASE_SIZE) + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_east is True:
                    coord = ((j + 1) * self.CASE_SIZE + self.MAZE_START[0],
                             i * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )
                if case.wall_south is True:
                    coord = (j * self.CASE_SIZE + self.MAZE_START[0],
                             (i + 1) * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_west is True:
                    coord = (j * self.CASE_SIZE + self.MAZE_START[0],
                             i * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )

    def load_pacgum(self) -> None:
        for pacgum in self.pacgum:
            sprite = pacgum.sprite
            pacgum_pos = self._position_entity_in_maze(pacgum, sprite)
            self.simulation_manager.screen.blit(
                source=sprite,
                dest=pacgum_pos
            )

    def load_ghosts(self) -> None:
        for ghost in self.ghosts:
            sprite = ghost.sprites[0][0]
            ghost_pos = self._position_entity_in_maze(ghost, sprite)
            self.simulation_manager.screen.blit(
                source=ghost.get_chasing_sprite(),
                dest=ghost_pos
            )

    def load_pacman(self) -> None:
        sprite = self.pacman.pacman_moving_sprites[0][0]
        pacman_pos = self._position_entity_in_maze(self.pacman, sprite)
        self.simulation_manager.screen.blit(
            source=self.pacman.get_moving_sprite(),
            dest=pacman_pos
        )

    def check_cooldown_timer(self):
        if self.super_pacgum_cooldown < time.monotonic():
            self.change_state(Character.State.RUNNING)

    def do_turn_consequences(self) -> None:
        self.check_cooldown_timer()
        self.eat_pacgum()
        self.ghost_collision()

    def eat_pacgum(self) -> None:
        case = self.maze.get_case(self.pacman.get_coord())
        if case.pacgum is None:
            return
        case.pacgum.eat(self.simulation_manager)
        self.pacgum.remove(case.pacgum)
        case.pacgum = None

    def ghost_collision(self):
        for ghost in self.ghosts:
            if not ghost.get_coord() == self.pacman.get_coord():
                continue
            if ghost.state == ghost.State.HUNTING:
                self.lives -= 1
                # start_coord = self.pacman.starting_position
                # self.pacman.line_pos = start_coord[0]
                # self.pacman.column_pos = start_coord[1]
            else:
                start_coord = ghost.starting_position
                ghost.line_pos = start_coord[0]
                ghost.column_pos = start_coord[1]
                self.simulation_manager.game_state.score +=\
                    self.simulation_manager.game_state.points_per_ghost

    def display_screen(self) -> None:
        self.move_pacman()
        self.move_ghosts()
        self.do_turn_consequences()
        self.load_maze()
        self.load_pacgum()
        self.load_pacman()
        self.load_ghosts()

    def _position_entity_in_maze(self, entity: Entity, sprite: pygame.Surface)\
            -> tuple[int, int]:
        return (
                ((self.MAZE_START[0] + (self.CASE_SIZE * entity.column_pos)) +
                    (self.CASE_SIZE // 2) - (sprite.get_width() // 2)),
                ((self.MAZE_START[1] + (self.CASE_SIZE * entity.line_pos)) +
                    (self.CASE_SIZE // 2) - (sprite.get_height() // 2))
            )

    def create_pacgums(self) -> None:
        nb_pacgum = self.simulation_manager.game_state.pacgum
        nb_super_pacgum = self.simulation_manager.game_state.super_pacgum
        nb_cases = self.maze.nb_column * self.maze.nb_line
        order_pacgum = list(range(nb_cases))
        random.shuffle(order_pacgum)
        for location in order_pacgum:
            line = location // self.maze.nb_column
            column = location % self.maze.nb_column
            case = self.maze.get_case((line, column))
            if case.is_enclosed is True or case.pacgum is not None:
                continue
            if nb_super_pacgum > 0:
                super_pacgum = SuperPacgum(line, column)
                self.pacgum.append(super_pacgum)
                case.pacgum = super_pacgum
                nb_super_pacgum -= 1
                continue
            if nb_pacgum > 0:
                pacgum = Pacgum(line, column)
                self.pacgum.append(pacgum)
                case.pacgum = pacgum
                nb_pacgum -= 1
                continue

    def change_state(self, state: Character.State) -> None:
        if state == Character.State.HUNTING:
            self.pacman.state = Character.State.HUNTING
            for ghost in self.ghosts:
                ghost.state = Character.State.RUNNING
        else:
            self.pacman.state = Character.State.RUNNING
            for ghost in self.ghosts:
                ghost.state = Character.State.HUNTING
