from . import Screen
import pygame


class Victory(Screen):
    def __init__(self, score: int) -> None:
        self.score: int = score
        self.font: pygame.font.Font = pygame.font.Font(None, 80)

    def display_screen(self) -> None:  # TODO
        self.simulation.screen.fill((0, 0, 0))
        congrat_message = self.font.render(
            "Congratulation", 1, (255, 255, 255)
            )
        self.simulation_manager.screen.blit(congrat_message,
                                            (750 - congrat_message.get_width(),
                                             400))
