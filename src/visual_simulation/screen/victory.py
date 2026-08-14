from . import LeaderBoard, Screen
import pygame


class Victory(Screen):
    def __init__(self, score: int, leaderboard: LeaderBoard) -> None:
        self.score: int = score

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
