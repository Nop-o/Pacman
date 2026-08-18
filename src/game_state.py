from .entity.character import Character
from .entity.pacman import Pacman
from .entity.ghost import Ghost
from .algorithm import DepthFirstSearch
from .maze import Maze


class GameState:

    def __init__(self, pacgum: int, points_per_pacgum: int,
                 points_per_super_pacgum: int, super_pacgum_time: int,
                 points_per_ghost: int, seed: int, level_max_time: int,
                 pacman: Pacman, ghosts: list[Ghost],
                 algorithm: DepthFirstSearch, maze: Maze) -> None:
        self.pacgum: int = pacgum
        self.super_pacgum: int = 4
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum
        self.super_pacgum_time: int = super_pacgum_time
        self.points_per_ghost: int = points_per_ghost
        self.seed: int = seed
        self.level_max_time: int = level_max_time
        self.pacman: Pacman = pacman
        self.ghosts: list[Ghost] = ghosts
        self.score: int = 0
        self.algorithm: DepthFirstSearch = DepthFirstSearch(maze)

    def pacman_eat_pacgum(self) -> None:
        """Update pacgum count and score after pacman eats a pacgum"""
        self.pacgum = self.pacgum - 1
        self.score = self.score + self.points_per_pacgum

    def pacman_eat_super_pacgum(self) -> None:
        """
        Update super pacgum count and score after pacman eats a super pacgum.
        Change pacman and ghost state."""
        self.super_pacgum = self.super_pacgum - 1
        self.score = self.score + self.points_per_super_pacgum

        if self.pacman.state == Character.State.RUNNING:
            self.pacman.change_state()
            for ghost in self.ghosts:
                ghost.change_state()

        self.pacman.reset_super_pacgum_cooldown()
        for ghost in self.ghosts:
            ghost.reset_super_pacgum_cooldown()
