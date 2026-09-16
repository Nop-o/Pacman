from .parsing import JsonData


class GameState:

    def __init__(self, json_data: JsonData) -> None:
        self.super_pacgum: int = 4
        self.score: int = 0
        self.pacgum: int = json_data.pacgum
        self.points_per_pacgum: int = json_data.points_per_pacgum
        self.points_per_super_pacgum: int = json_data.points_per_super_pacgum
        self.super_pacgum_cooldown: int = json_data.super_pacgum_cooldown
        self.points_per_ghost: int = json_data.points_per_ghost
        self.starting_seed: int = json_data.seed
        self.seed: int = json_data.seed
        self.level_max_time: int = json_data.level_max_time
        self.max_lives: int = json_data.lives
        self.current_lives: int = json_data.lives
        self.nb_level: int = 1

        self.is_game_over: bool = False
        self.is_game_won: bool = False

    def reset_game_state(self) -> None:
        self.score = 0
        self.super_pacgum = 4
        self.is_game_over = False
        self.is_game_won = False
        self.current_pacgum_count = self.pacgum
        self.current_lives = self.max_lives
        self.nb_level = 1
        self.seed = self.starting_seed
