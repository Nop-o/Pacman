from .pacman import Pacman
from . import Character
from ..algorithm.dfs import DepthFirstSearch
import random
from ..maze import Maze, Direction
from abc import ABC, abstractmethod
import pygame


class Ghost(Character, ABC):

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, super_pacgum_cooldown)
        self.pacman: Pacman = pacman
        self.freeze: bool = False
        self.algorithm: DepthFirstSearch = algorithm
        self._shortest_path_to_goal: list[tuple[int, int]] | None = None

        self.ghost_running_away_sprites: list[list[pygame.Surface]] = [
            [self.get_sprite("png/entities_sprite.png", 1, 554 + (i * 50),
             35, 35)
             for i in range(0, 2, 1)],
            [self.get_sprite("png/entities_sprite.png", 51, 554 + (i * 50),
             35, 35)
             for i in range(0, 2, 1)],
             ]

    @abstractmethod
    def get_goal(self) -> tuple[int, int]:
        """Decide if the ghost run away or chase pacman"""
        ...

    # def get_running_ghost_sprites(self) -> list[pygame.Surface]:
    #     running_ghost_sprites: list[pygame.Surface] = [
    #         self.running_away_1, self.running_away_2]

    #     if self.super_pacgum_cooldown > 5:
    #         running_ghost_sprites.extend(
    #             [self.running_away_3, self.running_away_4])

    #     return running_ghost_sprites

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line_pos, self.column_pos = self.starting_position

    def change_exit_position(self, new_goal: tuple[int, int]) -> None:
        """Update exit position"""
        self.algorithm.set_exit(new_goal)

    def change_entry_position(self) -> None:
        """Update entry position"""
        self.algorithm.set_entry((self.line_pos, self.column_pos))

    def find_shortest_path_to_exit(self) -> None:
        """Update solver"""
        self._shortest_path_to_goal = self.algorithm.solver()

    def do_turn(self) -> None:
        self.algorithm.set_entry(self.get_coord())
        self.algorithm.set_exit(self.get_goal())
        self.find_shortest_path_to_exit()
        if self.shortest_path_to_goal is None:
            raise ValueError("shortest_path_to_goal cannot be None")
        direction =\
            self.maze.get_direction_between_case(
                self.maze.get_case(self.get_coord()),
                self.maze.get_case(self.shortest_path_to_goal[0])
                )
        if direction is None:
            raise ValueError("direction cannot be None")
        self.move(direction)

    @property
    def shortest_path_to_goal(self) -> list[tuple[int, int]] | None:
        """Get _shortest_path_to_goal"""
        if self._shortest_path_to_goal is None:
            raise ValueError(
                f"{type(self).__name__} doesn't have a path to its goal")

        return self._shortest_path_to_goal

    def run_away(self) -> tuple[int, int]:
        """Update exit position to the furthest corner of the maze"""
        if self.pacman.line_pos <= len(self.maze.cases) // 2:
            if self.pacman.column_pos <= len(self.maze.cases[0]) // 2:
                return (0, 0)
            else:
                return (0, self.maze.nb_column - 1)
        else:
            if self.pacman.column_pos <= len(self.maze.cases[0]) // 2:
                return (self.maze.nb_line - 1, 0)
            else:
                return (self.maze.nb_line - 1, self.maze.nb_column - 1)

    def chase_pacman(self) -> tuple[int, int]:
        """Update exit position to pacman position"""
        return (self.pacman.line_pos, self.pacman.column_pos)


class Shadow(Ghost):  # red chase

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.shadow_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
             "png/entities_sprite.png", 1, 4 + (i * 50), 35, 35)
             for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 1, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Overwrite the abstract method of Ghost class"""
        if self.state == Character.State.RUNNING:
            return self.run_away()

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        return (0, 0)


class Speedy(Ghost):  # pink flank

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.speedy_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
              "png/entities_sprite.png", 51, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 51, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Overwrite the abstract method of Ghost class"""
        if self.state == Character.State.RUNNING:
            return self.run_away()

        for cardinal_point in Direction:
            if self.pacman.last_move_direction == cardinal_point:
                for i in range(3, 0, -1):
                    new_line_pos = cardinal_point.value[0] * i
                    new_column_pos = cardinal_point.value[1] * i

                    if self.maze.is_accessible(new_line_pos, new_column_pos):
                        return (new_line_pos, new_column_pos)

        return self.chase_pacman()

    def _set_starting_position(self) -> tuple[int, int]:
        return (0, self.maze.nb_column)


class Bashful(Ghost):  # cyan random

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.bashful_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
              "png/entities_sprite.png", 101, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 101, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Overwrite the abstract method of Ghost class"""
        if self.state == Character.State.RUNNING:
            return self.run_away()

        new_line = -1
        new_column = -1

        while not self.maze.is_accessible(new_line, new_column):
            new_line = random.randint(0, self.maze.nb_line)
            new_column = random.randint(0, self.maze.nb_column)
        return (new_line, new_column)

    def _set_starting_position(self) -> tuple[int, int]:
        return (self.maze.nb_line, 0)


class Pokey(Ghost):  # orange chase + run away

    def __init__(self, maze: Maze, pacman: Pacman, super_pacgum_cooldown: int,
                 algorithm: DepthFirstSearch) -> None:
        super().__init__(maze, pacman, super_pacgum_cooldown, algorithm)
        self.starting_position: tuple[int, int] = self._set_starting_position()

        self.pokey_sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
              "png/entities_sprite.png", 151, 4 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 104 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 204 + (i * 50), 35, 35)
              for i in range(0, 2, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 151, 304 + (i * 50), 35, 35)
              for i in range(0, 2, 1)]]

    def get_goal(self) -> tuple[int, int]:
        """Overwrite the abstract method of Ghost class"""
        if self.state == Character.State.RUNNING or self.is_pacman_too_close():
            return self.run_away()
        else:
            return self.chase_pacman()

    def is_pacman_too_close(self) -> bool:
        if (self.line_pos - self.pacman.line_pos < 3 and
           self.line_pos - self.pacman.line_pos > -3):
            if (self.column_pos - self.pacman.column_pos < 3 and
               self.column_pos - self.pacman.column_pos > -3):
                return True
        return False

    def _set_starting_position(self) -> tuple[int, int]:
        return (self.maze.nb_line, self.maze.nb_column)
