import pygame


class Fruit:
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        self.sprites: pygame.Surface = self.get_sprite(
            file_path, x, y, width, height)

    def get_sprite(self, file_path: str, x: int, y: int,
                   width: int, height: int) -> pygame.Surface:
        source_image = pygame.image.load(file_path).convert_alpha()

        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(source_image, (0, 0), (x, y, width, height))

        return image


class FruitManager:
    def __init__(self) -> None:
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
        if not self.fruit_position:
            self.update_fruit_position

        screen.blit(self.fruits[self.current_fruit].sprites,
                    self.fruit_position)

    def update_current_fruit(self) -> None:
        if self.current_fruit < len(self.fruits) - 1:
            self.current_fruit += 1
        else:
            self.current_fruit = 0

    def update_current_position(self) -> None:
        if self.current_position == 0:
            self.current_position = 1
        else:
            self.current_position = 0

    def ate_fruit(self) -> None:
        self.update_current_position()
        self.update_current_fruit()

    @property
    def fruit_position(self) -> tuple[int, int]:
        if not self._fruit_position:
            raise ValueError("Entity error: fruit position isn't known")
        return self._fruit_position[self.current_position]

    def set_fruit_position(self, positions: list[tuple[int, int]]) -> None:
        self._fruit_position = positions


class Cherry(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Strawberry(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Apricot(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Apple(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Berry(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Banana(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)


class Peach(Fruit):
    def __init__(self, file_path: str, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(file_path, x, y, width, height)
