import pygame


class TextRendering:
    """Renders text surfaces using a fixed set of font sizes."""

    def __init__(self) -> None:
        """Load the fonts used for regular text and titles of various sizes."""
        self.regular_text: pygame.font.Font = pygame.font.Font(None, 50)
        self.small_title: pygame.font.Font = pygame.font.Font(None, 80)
        self.medium_title: pygame.font.Font = pygame.font.Font(None, 130)
        self.big_title: pygame.font.Font = pygame.font.Font(None, 200)

    @staticmethod
    def render_text(text: str, color: tuple[int, int, int],
                    font: pygame.font.Font) -> pygame.Surface:
        """Render text using a given font and color.

        Args:
            text: The text to render.
            color: RGB color of the text.
            font: The font to render the text with.

        Returns:
            The rendered text surface.
        """
        return font.render(text, 1, color)

    def render_regular_text(
       self, text: str, color: tuple[int, int, int]) -> pygame.Surface:
        """Render text using the regular font.

        Args:
            text: The text to render.
            color: RGB color of the text.

        Returns:
            The rendered text surface.
        """
        return self.render_text(text, color, self.regular_text)

    def render_small_title(
       self, text: str, color: tuple[int, int, int]) -> pygame.Surface:
        """Render text using the small title font.

        Args:
            text: The text to render.
            color: RGB color of the text.

        Returns:
            The rendered text surface.
        """
        return self.render_text(text, color, self.small_title)

    def render_medium_title(
       self, text: str, color: tuple[int, int, int]) -> pygame.Surface:
        """Render text using the medium title font.

        Args:
            text: The text to render.
            color: RGB color of the text.

        Returns:
            The rendered text surface.
        """
        return self.render_text(text, color, self.medium_title)

    def render_big_title(
       self, text: str, color: tuple[int, int, int]) -> pygame.Surface:
        """Render text using the big title font.

        Args:
            text: The text to render.
            color: RGB color of the text.

        Returns:
            The rendered text surface.
        """
        return self.render_text(text, color, self.big_title)
