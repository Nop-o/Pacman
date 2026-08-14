from . import LeaderBoard, Screen
import pygame


class GameOver(Screen):
    def __init__(self, leaderboard: LeaderBoard) -> None:
        self.leaderboard: LeaderBoard = LeaderBoard

    def display_screen(self) -> bool:  # TODO
        pass

    def event_manager(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.show_leaderboard()

        return False


if __name__ == "__main__":
    leaderboard = LeaderBoard()
    game_over = GameOver(leaderboard)
