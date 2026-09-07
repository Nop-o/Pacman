import pygame


class TextRendering:
    def __init__(self) -> None:  # TODO add more text and test the current one
        self.regular_text: pygame.font.Font = pygame.font.Font(None, 30)
        self.small_title: pygame.font.Font = pygame.font.Font(None, 80)
        self.small_pacman: pygame.font.Font = pygame.font.Font(None, 120)
        self.big_pacman: pygame.font.Font = pygame.font.Font(None, 350)

    @staticmethod
    def render_text(text: str, color: tuple[int, int, int],
                    font: pygame.font.Font) -> pygame.Surface:
        return font.render(text, 1, color)

    def render_regular_text(self, text: str,
                            color: tuple[int, int, int]) -> pygame.Surface:
        return self.render_text(text, color, self.regular_text)

    def render_small_title(self, text: str,
                           color: tuple[int, int, int]) -> pygame.Surface:
        return self.render_text(text, color, self.small_title)

    def render_small_pacman(self, text: str,
                            color: tuple[int, int, int]) -> pygame.Surface:
        return self.render_text(text, color, self.small_pacman)

    def render_big_pacman(self, text: str,
                          color: tuple[int, int, int]) -> pygame.Surface:
        return self.render_text(text, color, self.big_pacman)
