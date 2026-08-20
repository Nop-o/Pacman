import pygame


class TextRendering:
    def __init__(self) -> None:
        self.regular_text: pygame.font.Font = pygame.font.Font(None, 30)
        self.small_title: pygame.font.Font = pygame.font.Font(None, 80)
        self.samll_pacman: pygame.font.Font = pygame.font.Font(None, 120)
        self.big_pacman: pygame.font.Font = pygame.font.Font(None, 150)
