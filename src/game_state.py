from src.entity import Pacman, Ghost, Entity


class GameState:
    def __init__(self, pacgum: int, points_per_pacgum: int,
                 points_per_super_pacgum: int, super_pacgum_time: int,
                 points_per_ghost: int, seed: int, level_max_time: int,
                 pacman: Pacman, ghosts: list[Ghost]) -> None:
        self.pacgum = pacgum
        self.super_pacgum = 4
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.super_pacgum_time = super_pacgum_time
        self.points_per_ghost = points_per_ghost
        self.seed = seed
        self.level_max_time = level_max_time
        self.pacman = pacman
        self.ghosts = ghosts
        self.score = 0

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

        if self.pacman.state == Entity.State.RUNNING:
            self.pacman.change_state()
            for ghost in self.ghosts:
                ghost.change_state()

        self.pacman.reset_super_pacgum_cooldown()
        for ghost in self.ghosts:
            ghost.reset_super_pacgum_cooldown()
