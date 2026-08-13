from time import time, sleep
import pygame
from collections.abc import Callable
from .screen_manager import ScreenManager


class SimulationManager():
    def __init__(self, screen_manager: ScreenManager) -> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.fps: int = 60
        self.frame_duration: float = 1.0 / self.fps
        self.screen: pygame.Surface = pygame.display.set_mode(
            (1500, 1000), pygame.RESIZABLE)
        # TODO set basic function to main menu
        self.test = Test(self)
        self.state_to_call: Callable = self.test.test1
        self.active = True
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.screen_manager = screen_manager

    def launch(self) -> None:
        while self.active:
            start_time = time()
            self.state_to_call()
            self.display_on_screen()

            self.event_manager()
            elapsed = time() - start_time
            if elapsed < self.frame_duration:
                sleep(self.frame_duration - elapsed)

    def clear_last_frame(self, color: str = "black") -> None:
        """Clear the last frame, recover it with a screen with a color"""
        self.screen.fill(pygame.Color(color))

    @staticmethod
    def display_on_screen() -> None:
        """Display everything that you prepared to the screen"""
        pygame.display.flip()

    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.screen_manager.pause_menu
                    pass
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                if event.key == pygame.K_DOWN:
                    self.down_pressed = True
                if event.key == pygame.K_UP:
                    self.up_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                if event.key == pygame.K_DOWN:
                    self.down_pressed = False
                if event.key == pygame.K_UP:
                    self.up_pressed = False

    def draw_rectangle(self, coord: tuple[int, int],
                       width: int, height: int, color: tuple[int, int, int]):
        for actual_width in range(width):
            for actual_height in range(height):
                self.screen.set_at(
                    ((actual_width + coord[0]),
                     (actual_height + coord[1])), color)


if __name__ == "__main__":
    class Test():
        def __init__(self, simulation_manager: SimulationManager) -> None:
            self.simulation_manager = simulation_manager
            self.color: tuple = (0, 0, 0)
            self.horizontal = 0

        def test1(self):
            screen = self.simulation_manager.screen
            screen.fill("black")
            if self.simulation_manager.left_pressed:
                self.horizontal -= 1
            if self.simulation_manager.right_pressed:
                self.horizontal += 1

            self.simulation_manager.draw_rectangle((500, 500), 333, 666,
                                                   self.color)

            self.color = (self.color[0] + 1,
                          self.color[1] + 1,
                          self.color[2] + 1)
            if self.color[0] == 255:
                self.simulation_manager.state_to_call = self.test2

        def test2(self):
            screen = self.simulation_manager.screen
            screen.fill("white")

            if self.simulation_manager.left_pressed:
                self.horizontal -= 1
            if self.simulation_manager.right_pressed:
                self.horizontal += 1

            self.simulation_manager.draw_rectangle((500, 500), 333, 666,
                                                   self.color)

            self.color = (self.color[0] - 1,
                          self.color[1] - 1,
                          self.color[2] - 1)
            if self.color[0] == 0:
                self.simulation_manager.state_to_call = self.test1
    simulation = SimulationManager()
    simulation.launch()
