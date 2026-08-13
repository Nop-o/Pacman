from .game_play import GamePlay
from .leaderboard import LeaderBoard
from .screen import Screen


class MainMenu(Screen):
    def __init__(self, game_play: GamePlay, leaderboard: LeaderBoard) -> None:
        self.game_play: GamePlay = GamePlay
        self.leaderboard: leaderboard = LeaderBoard

    def show_instructions(self) -> None:  # TODO
        pass

    def display_screen(self) -> bool:  # TODO
        pass

    def event_manager(self) -> bool:
        actions: list[callable] = [
            self.resume_game,
            self.show_leaderboard,
            self.show_instructions,
            self.exit_game,
        ]
        position: int = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if position < 3:
                        position = position + 1
                    else:
                        position = 0

                if event.key == pygame.K_UP:
                    if position > 0:
                        position = position - 1
                    else:
                        position = 3

                if event.key == pygame.K_RETURN:
                    return actions[position]()

        return False
