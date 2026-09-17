import pygame


class Fruit:
    """A collectible fruit backed by a sprite."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the fruit's sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        self.sprites: pygame.Surface = self.get_sprite(
            file_path, x, y, width, height)

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        """Extract a sprite region from a sprite sheet image.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.

        Returns:
            A surface containing the extracted sprite, with alpha channel.
        """
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image


class FruitManager:
    """Manage the cycle of fruits displayed in the maze."""

    def __init__(self) -> None:
        """Initialize the fruit sprites and cycling state."""
        self.fruits: list[Fruit] = [
            Cherry("png/entities_sprite.png", 601, 4, 35, 35),
            Strawberry("png/entities_sprite.png", 601, 54, 35, 35),
            Apricot("png/entities_sprite.png", 601, 104, 35, 35),
            Apple("png/entities_sprite.png", 601, 154, 35, 35),
            Berry("png/entities_sprite.png", 601, 204, 35, 35),
            Banana("png/entities_sprite.png", 601, 254, 35, 35),
            Peach("png/entities_sprite.png", 601, 304, 35, 35)
        ]

        self._fruit_position: list[tuple[int, int]]
        self.current_fruit: int = 0
        self.current_position: int = 0

    def display_fruits(self, screen: pygame.Surface) -> None:
        """Draw the current fruit at its current position.

        Args:
            screen: Surface to draw on.
        """
        if not self.fruit_position:
            self.update_fruit_position

        screen.blit(self.fruits[self.current_fruit].sprites,
                    self.fruit_position)

    def update_current_fruit(self) -> None:
        """Advance to the next fruit in the cycle, wrapping around."""
        if self.current_fruit < len(self.fruits) - 1:
            self.current_fruit += 1
        else:
            self.current_fruit = 0

    def update_current_position(self) -> None:
        """Toggle the current fruit position between the two
        available slots."""
        if self.current_position == 0:
            self.current_position = 1
        else:
            self.current_position = 0

    def ate_fruit(self) -> None:
        """Advance the fruit position and fruit type after one is eaten."""
        self.update_current_position()
        self.update_current_fruit()

    @property
    def fruit_position(self) -> tuple[int, int]:
        """Return the current on-screen position of the displayed fruit.

        Returns:
            The (x, y) position of the current fruit.

        Raises:
            ValueError: If the fruit positions have not been set.
        """
        if not self._fruit_position:
            raise ValueError("Entity error: fruit position isn't known")
        return self._fruit_position[self.current_position]

    def set_fruit_position(self, positions: list[tuple[int, int]]) -> None:
        """Set the available on-screen fruit positions.

        Args:
            positions: List of (x, y) positions fruits can be displayed at.
        """
        self._fruit_position = positions


class Cherry(Fruit):
    """A cherry fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the cherry sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Strawberry(Fruit):
    """A strawberry fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the strawberry sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Apricot(Fruit):
    """An apricot fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the apricot sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Apple(Fruit):
    """An apple fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the apple sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Berry(Fruit):
    """A berry fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the berry sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Banana(Fruit):
    """A banana fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the banana sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)


class Peach(Fruit):
    """A peach fruit."""

    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        """Load the peach sprite from a sprite sheet region.

        Args:
            file_path: Path to the sprite sheet image.
            x: X coordinate of the sprite region within the sheet.
            y: Y coordinate of the sprite region within the sheet.
            width: Width of the sprite region.
            height: Height of the sprite region.
        """
        super().__init__(file_path, x, y, width, height)
