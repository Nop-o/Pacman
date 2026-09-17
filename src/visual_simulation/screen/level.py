from .screen import Screen
from typing import TYPE_CHECKING
from ...maze import Direction, Maze
from ...entity import Ghost, Pacman, Shadow, Speedy, Bashful, Pokey
from ...algorithm import DepthFirstSearch
from ...entity import Entity, Pacgum, SuperPacgum, Character
from ... import Cheat
import pygame
import random
import time

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class Level(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:

        self.simulation_manager: SimulationManager = simulation_manager
        self.maze: Maze = Maze(self.simulation_manager.game_state.seed)
        self.algo = DepthFirstSearch(self.maze)
        self.cheat: Cheat = Cheat(self.simulation_manager)
        super_pacgum_cooldown =\
            self.simulation_manager.game_state.super_pacgum_cooldown
        self.pacman: Pacman = Pacman(self.maze, super_pacgum_cooldown)
        self.ghosts: list[Ghost] = []
        self.ghosts.append(Shadow(self.maze, self.pacman,
                                  super_pacgum_cooldown, self.algo))
        self.ghosts.append(Speedy(self.maze, self.pacman,
                                  super_pacgum_cooldown, self.algo))
        self.ghosts.append(Bashful(self.maze, self.pacman,
                                   super_pacgum_cooldown, self.algo))
        self.ghosts.append(Pokey(self.maze, self.pacman,
                                 super_pacgum_cooldown, self.algo))
        self.pacgum: list[Pacgum] = []
        self.create_pacgums()
        self.CASE_SIZE = 50
        self.CASE_LINE_THICKNESS = 3
        self.MAZE_WIDTH = (self.CASE_SIZE) * self.maze.nb_column
        self.MAZE_HEIGHT = (self.CASE_SIZE) * self.maze.nb_line
        self.MAZE_START = (self.simulation_manager.screen_width // 2 -
                           self.MAZE_WIDTH // 2,
                           self.simulation_manager.screen_height // 2 -
                           self.MAZE_HEIGHT // 2 - 50
                           )
        self.MAZE_END = (self.MAZE_START[0] + self.MAZE_WIDTH,
                         self.MAZE_START[1] + self.MAZE_HEIGHT)
        self.super_pacgum_cooldown: float | None = 0
        self.move_timer: float = 0.4
        self.time_elapse: float = 0
        self.last_frame_time: float | None = None
        self.sprite_timer: float = 0.20
        self.sprite_time_elapse: float = 0
        self.level_timer: float = 0

    def move_pacman(self) -> None:
        if self.simulation_manager.up_pressed:
            self.pacman.move(Direction.N)
        elif self.simulation_manager.right_pressed:
            self.pacman.move(Direction.E)
        elif self.simulation_manager.down_pressed:
            self.pacman.move(Direction.S)
        elif self.simulation_manager.left_pressed:
            self.pacman.move(Direction.W)
        else:
            self.pacman.move(None)

    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            if ghost.death_timer is not None:
                continue
            if self.cheat.is_ghost_freeze is True:
                return
            ghost.do_turn()

    def load_maze(self) -> None:
        for i, line in enumerate(self.maze.cases):
            for j, case in enumerate(line):
                if case.wall_north is True:
                    coord = ((j * self.CASE_SIZE) + self.MAZE_START[0],
                             (i * self.CASE_SIZE) + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_east is True:
                    coord = ((j + 1) * self.CASE_SIZE + self.MAZE_START[0],
                             i * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )
                if case.wall_south is True:
                    coord = (j * self.CASE_SIZE + self.MAZE_START[0],
                             (i + 1) * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_SIZE,
                                        height=self.CASE_LINE_THICKNESS,
                                        color=(255, 255, 255),
                                        center_height=True
                                        )
                if case.wall_west is True:
                    coord = (j * self.CASE_SIZE + self.MAZE_START[0],
                             i * self.CASE_SIZE + self.MAZE_START[1])
                    self.draw_rectangle(coord=coord,
                                        width=self.CASE_LINE_THICKNESS,
                                        height=self.CASE_SIZE,
                                        color=(255, 255, 255),
                                        center_width=True
                                        )

    def load_pacgum(self) -> None:
        for pacgum in self.pacgum:
            sprite = pacgum.sprite
            pacgum_pos = self._position_entity_in_maze(pacgum, sprite)
            self.simulation_manager.screen.blit(
                source=sprite,
                dest=pacgum_pos
            )

    def load_ghosts(self) -> None:
        for ghost in self.ghosts:
            if ghost.death_timer is not None:
                continue
            sprite = ghost.sprites[0][0]
            if self.cheat.is_ghost_freeze is True:
                ghost_pos = (
                    ((self.MAZE_START[0] +
                        (self.CASE_SIZE * ghost.prev_column_pos)) +
                        (self.CASE_SIZE // 2) - (sprite.get_width() // 2)),
                    ((self.MAZE_START[1] +
                        (self.CASE_SIZE * ghost.prev_line_pos)) +
                        (self.CASE_SIZE // 2) - (sprite.get_height() // 2))
                )
            else:
                ghost_pos = self._position_entity_in_maze(ghost, sprite)
            self.simulation_manager.screen.blit(
                source=ghost.get_valid_sprite(),
                dest=ghost_pos
            )

    def load_pacman(self) -> None:
        sprite = self.pacman.sprites[0][0]
        pacman_pos = self._position_entity_in_maze(self.pacman, sprite)
        self.simulation_manager.screen.blit(
            source=self.pacman.get_moving_sprite(),
            dest=pacman_pos
        )

    def check_cooldown_timer(self) -> None:
        if self.super_pacgum_cooldown is None:
            return
        if self.super_pacgum_cooldown < time.monotonic():
            self.change_state(Character.State.RUNNING)

    def do_turn_consequences(self) -> None:
        self.check_cooldown_timer()
        self.eat_pacgum()
        self.ghost_collision()
        if self.simulation_manager.game_state.current_lives <= 0:
            self.simulation_manager.game_state.is_game_over = True
        if len(self.pacgum) == 0:
            self.simulation_manager.game_state.is_game_won = True

    def eat_pacgum(self) -> None:
        case = self.maze.get_case(self.pacman.get_coord())
        if case.pacgum is None:
            return
        case.pacgum.eat(self.simulation_manager)
        self.pacgum.remove(case.pacgum)
        case.pacgum = None

    def ghost_collision(self) -> None:
        for ghost in self.ghosts:
            if ghost.death_timer is not None:
                continue
            if not ghost.get_coord() == self.pacman.get_coord():
                continue
            if ghost.state == ghost.State.HUNTING:
                if self.cheat.is_invicible == True:
                    continue
                self.simulation_manager.game_state.current_lives -= 1
                start_coord = self.pacman.starting_position
                self.pacman.line_pos = start_coord[0]
                self.pacman.column_pos = start_coord[1]
                for gh in self.ghosts:
                    gh.reset_starting_position()
            else:
                ghost.die()
                self.simulation_manager.game_state.score +=\
                    self.simulation_manager.game_state.points_per_ghost

    def display_screen(self) -> None:
        now = time.monotonic()
        if self.last_frame_time is None:
            self.last_frame_time = now
        delta = now - self.last_frame_time
        self.time_elapse += delta
        self.sprite_time_elapse += delta
        self.last_frame_time = now
        self.check_level_timer(delta)
        self.check_ghost_death(delta)
        if self.check_action_timer():
            self.do_turn_consequences()
            self.move_pacman()
            self.move_ghosts()
        if self.check_sprite_timer():
            self.pacman.update_state_of_sprite()
            for ghost in self.ghosts:
                ghost.update_state_of_sprite()
        self.load_maze()
        self.load_pacgum()
        self.load_pacman()
        self.load_ghosts()
        self.load_cheat_panel()

    def check_ghost_death(self, delta: float) -> None:
        for ghost in self.ghosts:
            if ghost.death_timer is None:
                continue
            ghost.death_timer -= delta
            if ghost.death_timer <= 0:
                ghost.death_timer = None

    def _position_character_in_maze(self, entity: Character,
                                    sprite: pygame.Surface) -> tuple[int, int]:
        progress = min(self.time_elapse / self.move_timer, 1.0)
        if (entity.column_pos == entity.prev_column_pos and
                entity.line_pos == entity.prev_line_pos):
            progress_modifier = (0, 0)
        elif entity.prev_direction == Character.FacingDirection.UP:
            progress_modifier = (0, int(0 - self.CASE_SIZE * progress))
        elif entity.prev_direction == Character.FacingDirection.RIGHT:
            progress_modifier = (int(0 + self.CASE_SIZE * progress), 0)
        elif entity.prev_direction == Character.FacingDirection.DOWN:
            progress_modifier = (0, int(0 + self.CASE_SIZE * progress))
        else:
            progress_modifier = (int(0 - self.CASE_SIZE * progress), 0)
        return (
                int(((self.MAZE_START[0] +
                    (self.CASE_SIZE * entity.prev_column_pos)) +
                    (self.CASE_SIZE // 2) - (sprite.get_width() // 2)
                    + progress_modifier[0])),
                int(((self.MAZE_START[1] +
                    (self.CASE_SIZE * entity.prev_line_pos)) +
                    (self.CASE_SIZE // 2) - (sprite.get_height() // 2)
                    + progress_modifier[1]))
            )
    def _position_in_maze(self, entity: Entity, sprite: pygame.Surface)\
            -> tuple[int, int]:
        return (
                    ((self.MAZE_START[0] +
                        (self.CASE_SIZE * entity.column_pos)) +
                        (self.CASE_SIZE // 2) - (sprite.get_width() // 2)),
                    ((self.MAZE_START[1] +
                        (self.CASE_SIZE * entity.line_pos)) +
                        (self.CASE_SIZE // 2) - (sprite.get_height() // 2))
                )

    def _position_entity_in_maze(self, entity: Entity, sprite: pygame.Surface)\
            -> tuple[int, int]:
        if (not isinstance(entity, Character) or
            (entity.prev_column_pos == entity.column_pos
                and entity.line_pos == entity.prev_line_pos)):
            return self._position_in_maze(entity, sprite)
        return self._position_character_in_maze(entity, sprite)

    def create_pacgums(self) -> None:
        nb_pacgum = self.simulation_manager.game_state.pacgum
        nb_cases = self.maze.nb_column * self.maze.nb_line
        order_pacgum = list(range(nb_cases))
        random.shuffle(order_pacgum)
        nb_column = self.maze.nb_column - 1
        nb_line = self.maze.nb_line - 1

        super_pacgum_1 = SuperPacgum(0, 0)
        super_pacgum_2 = SuperPacgum(nb_line, 0)
        super_pacgum_3 = SuperPacgum(0, nb_column)
        super_pacgum_4 = SuperPacgum(nb_column, nb_line)

        self.maze.cases[0][0].pacgum = super_pacgum_1
        self.maze.cases[nb_line][0].pacgum = super_pacgum_2
        self.maze.cases[0][nb_column].pacgum = super_pacgum_3
        self.maze.cases[nb_line][nb_column].pacgum = super_pacgum_4

        self.pacgum.append(super_pacgum_1)
        self.pacgum.append(super_pacgum_2)
        self.pacgum.append(super_pacgum_3)
        self.pacgum.append(super_pacgum_4)

        for location in order_pacgum:
            line = location // self.maze.nb_column
            column = location % self.maze.nb_column
            case = self.maze.get_case((line, column))
            if case.is_enclosed is True or case.pacgum is not None:
                continue
            if nb_pacgum > 0:
                pacgum = Pacgum(line, column)
                self.pacgum.append(pacgum)
                case.pacgum = pacgum
                nb_pacgum -= 1
                continue

    def change_state(self, state: Character.State) -> None:
        if state == Character.State.HUNTING:
            self.pacman.state = Character.State.HUNTING
            for ghost in self.ghosts:
                ghost.state = Character.State.RUNNING
                self.super_pacgum_cooldown = time.monotonic() +\
                    self.simulation_manager.game_state.super_pacgum_cooldown
                ghost.super_pacgum_cooldown = self.super_pacgum_cooldown
        else:
            self.pacman.state = Character.State.RUNNING
            for ghost in self.ghosts:
                ghost.state = Character.State.HUNTING
                ghost.super_pacgum_cooldown = None
                self.super_pacgum_cooldown = None

    def check_action_timer(self) -> bool:
        if self.time_elapse > self.move_timer:
            self.time_elapse -= self.move_timer
            return True
        return False

    def check_sprite_timer(self) -> bool:
        if self.sprite_time_elapse > self.sprite_timer:
            self.sprite_time_elapse -= self.sprite_timer
            return True
        return False

    def reset_timer(self) -> None:
        self.time_elapse = 0
        self.sprite_time_elapse = 0
        self.last_frame_time = None

    def check_level_timer(self, delta: float) -> None:
        if self.cheat.is_timer_freeze == True:
            return
        self.level_timer += delta
        game_state = self.simulation_manager.game_state
        if self.level_timer >= game_state.level_max_time:
            game_state.is_game_over = True

    def load_cheat_panel(self) -> None:
        if self.simulation_manager.game_state.is_cheat_active is False:
            return
        CHEAT_LIST = [
            "S - Skip level",
            "L - Extra life",
            "I - Invincibility",
            "F - Freeze ghosts",
            "T - Freeze timer",
        ]
        panel_x = self.MAZE_END[0] + 30
        panel_y = self.MAZE_START[1]
        for i, cheat_label in enumerate(CHEAT_LIST):
            text_surface = \
                self.simulation_manager.text_rendering.render_regular_text(
                    cheat_label, (255, 255, 0))
            self.simulation_manager.screen.blit(
                text_surface, (panel_x, panel_y + i * 60)
            )
