class GameState:

    def __init__(self, lives: int, pacgum: int, points_per_pacgum: int,
                 points_per_super_pacgum: int, super_pacgum_cooldown: int,
                 points_per_ghost: int, seed: int, level_max_time: int
                 ) -> None:

        self.pacgum: int = pacgum
        self.super_pacgum: int = 4
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum
        self.super_pacgum_cooldown: int = super_pacgum_cooldown
        self.points_per_ghost: int = points_per_ghost
        self.seed: int = seed
        self.level_max_time: int = level_max_time
        self.score: int = 0
        self.lives: int = lives

        self.is_game_over: bool = False
        self.is_game_won: bool = False

    # def pacman_eat_pacgum(self) -> None:
    #     """Update pacgum count and score after pacman eats a pacgum"""
    #     self.pacgum = self.pacgum - 1
    #     self.score = self.score + self.points_per_pacgum

    # def pacman_eat_super_pacgum(self) -> None:
    #     """
    #     Update super pacgum count and score after pacman eats a super pacgum.
    #     Change pacman and ghost state."""
    #     self.super_pacgum = self.super_pacgum - 1
    #     self.score = self.score + self.points_per_super_pacgum

    #     if self.pacman.state == Character.State.RUNNING:
    #         self.pacman.change_state()
    #         for ghost in self.ghosts:
    #             ghost.change_state()

    #     self.pacman.reset_super_pacgum_cooldown()
    #     for ghost in self.ghosts:
    #         ghost.reset_super_pacgum_cooldown()

    def reset_game_state(self) -> None:
        self.score = 0
        self.super_pacgum = 4
        self.is_game_over = False
        self.is_game_won = False
        self.current_pacgum_count = self.pacgum
