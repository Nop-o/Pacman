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
        self.max_lives: int = lives
        self.current_lives: int = lives
        self.nb_level: int = 1

        self.is_game_over: bool = False
        self.is_game_won: bool = False

    def reset_game_state(self) -> None:
        self.score = 0
        self.super_pacgum = 4
        self.is_game_over = False
        self.is_game_won = False
        self.current_pacgum_count = self.pacgum
