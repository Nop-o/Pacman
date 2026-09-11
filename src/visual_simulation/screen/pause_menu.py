from . import Screen
import pygame
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..simulation_manager import SimulationManager


class PauseMenu(Screen):
    def __init__(self, simulation_manager: "SimulationManager") -> None:
        super().__init__(simulation_manager=simulation_manager)
        self.current_choice_position: int = 0

        self.arcade_pacman: pygame.Surface = \
            self.simulation_manager.get_sprite(
                "png/arcade_pacman.png", 50, 10, 380, 800)

    def display_screen(self) -> None:
        self.simulation_manager.dipslay_sky()

        pause_menu_title = \
            self.simulation_manager.text_rendering.render_big_title(
                "Pause Menu", (255, 255, 0))
        resume_game_text = \
            self.simulation_manager.text_rendering.render_medium_title(
                "Resume Game", (255, 255, 0))
        main_menu_text = \
            self.simulation_manager.text_rendering.render_medium_title(
                "Return to the main menu", (255, 255, 0))
        exit_game_text = \
            self.simulation_manager.text_rendering.render_medium_title(
                "Exit Game", (255, 255, 0))

        title_padding: list[int] = self.simulation_manager.get_title_paddings(
            [pause_menu_title, resume_game_text,
             main_menu_text, exit_game_text], 10, 5
        )

        self.simulation_manager.screen.blit(pause_menu_title, (
            self.simulation_manager.get_center_width(pause_menu_title),
            title_padding[0]))
        self.simulation_manager.screen.blit(resume_game_text, (
            self.simulation_manager.get_center_width(resume_game_text),
            title_padding[1]))
        self.simulation_manager.screen.blit(main_menu_text, (
            self.simulation_manager.get_center_width(main_menu_text),
            title_padding[2]))
        self.simulation_manager.screen.blit(exit_game_text, (
            self.simulation_manager.get_center_width(exit_game_text),
            title_padding[3]))
        
        self.simulation_manager.screen.blit(self.arcade_pacman, (30, 520))

        self.simulation_manager.button_manager.display_buttons(
            self.simulation_manager.screen, [
                pause_menu_title, resume_game_text, main_menu_text,
                exit_game_text], title_padding, self.current_choice_position
        )

    def screen_selector(self, events: list[pygame.event.Event]) -> None:
        actions: list[Callable[[], None]] = [
            self.game_play_screen,
            self.main_menu_screen,
            self.exit_game,
        ]

        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.current_choice_position < 2:
                        self.current_choice_position += 1
                    else:
                        self.current_choice_position = 0

                if event.key == pygame.K_UP:
                    if self.current_choice_position > 0:
                        self.current_choice_position -= 1
                    else:
                        self.current_choice_position = 2

                if event.key == pygame.K_RETURN:
                    actions[self.current_choice_position]()
                    return
