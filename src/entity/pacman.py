from . import Character
from ..maze import Maze, Direction
import pygame


class Pacman(Character):

    def __init__(self, maze: Maze, super_pacgum_cooldown: int) -> None:
        super().__init__(maze, super_pacgum_cooldown, state_of_sprite=1)
        self._last_move_direction: Direction
        self.reset_last_move_direction()

        self.invincible: bool = False

        self.sprites: list[list[pygame.Surface]] = \
            [[self.get_sprite(
              "png/entities_sprite.png", 851, 4 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 154 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 304 + (i * 50), 35, 35)
              for i in range(0, 3, 1)],
             [self.get_sprite(
              "png/entities_sprite.png", 851, 454 + (i * 50), 35, 35)
              for i in range(0, 3, 1)]]

        self.pacman_dying_sprites: list[pygame.Surface] = \
            [self.get_sprite(
             "png/entities_sprite.png", 351, 4 + (i * 50), 35, 35)
             for i in range(0, 11, 1)]

    def _set_starting_position(self) -> tuple[int, int]:
        """Find the starting position of pacman, at the middle if possible"""
        line_pos = (len(self.maze.cases) - 1) // 2
        column_pos = (len(self.maze.cases[0]) - 1) // 2

        if self.verif_position(line_pos, column_pos):
            return (line_pos, column_pos)

        i = 1
        while True:
            j = 0
            while j < i:
                if self.verif_position(line_pos-i + j, column_pos-i):
                    return (line_pos-i + j, column_pos-i)
                if self.verif_position(line_pos-i, column_pos-i + j):
                    return (line_pos-i, column_pos-i + j)
                if self.verif_position(line_pos+i + j, column_pos-i):
                    return (line_pos+i + j, column_pos-i)
                if self.verif_position(line_pos+i, column_pos-i + j):
                    return (line_pos+i, column_pos-i + j)
                j += 1
            i += 1

    def verif_position(self, line_pos: int, column_pos: int) -> bool:
        if self.maze.cases[line_pos][column_pos].is_enclosed is False:
            self.line_pos = line_pos
            self.column_pos = column_pos
            return True
        return False

    def reset_starting_position(self) -> None:
        """Reset the position of an entity to his starting position"""
        self.line_pos, self.column_pos = self.starting_position

    @property
    def last_move_direction(self) -> Direction:
        return self._last_move_direction

    def reset_last_move_direction(self) -> None:
        self._last_move_direction = Direction.N

    def update_state_of_sprite(self) -> None:
        self.state_of_sprite += 1
        self.state_of_sprite %= 3

    def get_moving_sprite(self):
        sprite = self.sprites[self.direction][self.state_of_sprite]
        return sprite
